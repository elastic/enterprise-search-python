import re
import json
import sys
import pathlib
from typing import Optional, Mapping, List, Set
import jinja2

templates_dir = str(pathlib.Path(__file__).absolute().parent / "templates")
loader = jinja2.FileSystemLoader(templates_dir)
env = jinja2.Environment(
    loader=loader,
)
t = env.get_template("component")


def openapi_type_to_typing(openapi_type, required=True) -> str:
    t = None
    if openapi_type == "string":
        t = "str"
    elif openapi_type == "integer":
        t = "int"
    elif openapi_type == "number":
        t = "typing.Union[float, int]"
    elif openapi_type == "boolean":
        t = "bool"
    if t and not required:
        t = "typing.Optional[%s]" % t
    return t


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def to_python_param(name):
    name = re.sub(r"^[^a-z0-9_]*", "", name.lower())
    name = re.sub(r"[^a-z0-9_]*$", "", name)
    return re.sub(r"[^a-z0-9_]+", "_", name)


class Component:
    def __init__(self, openapi_name: str, openapi_type: str, component_namespace: str, properties: Optional[Mapping[str, "Component"]]=None, required_properties=None):
        self.openapi_name = openapi_name
        self.openapi_type = openapi_type
        self.component_namespace = component_namespace
        self.properties = properties or {}
        self.required_properties = required_properties or []

        # object and array must have properties
        if openapi_type == "object":
            #assert len(self.properties) > 0
            assert all(x in self.properties for x in self.required_properties)
        elif openapi_type == "array":
            assert tuple(self.properties) == ("items",)

    @property
    def class_name(self):
        if self.openapi_type == "object":
            return self.openapi_name.title().replace("_", "")
        return None

    @property
    def typing_type(self):
        t = openapi_type_to_typing(self.openapi_type)
        if t:
            return t
        elif self.openapi_type == "array":
            return f"typing.List[{self.properties['items'].typing_type}]"
        else:
            return self.class_name

    def __repr__(self):
        return f"<{self.openapi_name} {self.openapi_type} {self.component_namespace} {self.properties}>"

    @property
    def has_typing_import(self):
        # typing.List
        if self.openapi_type == "array":
            return True
        # typing.Optional
        elif self.openapi_type == "object" and list(self.properties) != self.required_properties:
            return True
        # Sub-components
        elif any(component.has_typing_import for component in self.properties.values()):
            return True
        return False

    @property
    def is_response(self):
        return "Response" in (self.class_name or ())

    @property
    def other_imports(self) -> Mapping[str, Set[str]]:
        imports = {}
        for key, component in self.properties.items():
            if not isinstance(component, Component):
                continue
            if component.component_namespace != self.component_namespace and component.class_name:
                imports.setdefault(f".{component.component_namespace}", set()).add(component.class_name)
        return imports

    def to_python(self) -> List[str]:
        if self.openapi_type != "object":
            return []
        return [x for x in env.get_template("component").render(component=self).split("\n") if x.strip()]


class ComponentNamespace:
    def __init__(self, name):
        self.name = name
        self.components = []

    @property
    def imports(self) -> List[str]:
        imports = []
        if any(component.has_typing_import for component in self.components):
            imports.append("from ..utils import typing")
        if any(component.is_response for component in self.components):
            imports.append("from ._base import JSONResponse")
        from_imports = {}
        for component in self.components:
            for key, imp in component.other_imports.items():
                from_imports[key] = from_imports.setdefault(key, set()).union(imp)
        for from_, names in sorted(from_imports.items()):
            imports.append(f"from {from_} import {', '.join(sorted(names))}")
        return imports

    def to_python(self) -> List[str]:
        code = []
        for component in self.components:
            code.extend(component.to_python())
        if code:
            code = self.imports + code
        return [x for x in code if x.strip()]


class APIParameter:
    def __init__(self, name, openapi_type, required, description, wire_name):
        self.name = name
        self.wire_name = wire_name
        self.openapi_type = openapi_type
        self.required = required
        self.description = description

    @property
    def typing_type(self):
        if self.openapi_type == "string":
            t = "str"
        elif self.openapi_type == "integer":
            t = "int"
        elif self.openapi_type == "number":
            t = "typing.Union[float, int]"
        elif self.openapi_type == "boolean":
            t= "bool"
        elif self.openapi_type == "array":
            t = "typing.List[%s]"
        else:
            raise ValueError("typing_type isn't defined")
        if not self.required:
            t = "typing.Optional[%s]" % t
        return t


class API:
    def __init__(self, name, method, path_parts, description, doc_url, has_body, path_params, query_params, response_class):
        self.name = name
        self.method = method
        self.path_parts = path_parts
        self.path_params = path_params
        self.query_params = query_params
        self.description = description
        self.doc_url = doc_url
        self.has_body = has_body
        self.response_class = response_class

    @property
    def required_params(self):
        assert all(x.required for x in self.path_params)
        return self.path_params

    @property
    def optional_params(self):
        assert not any(x.required for x in self.query_params)
        return self.query_params

    @property
    def all_params(self):
        return self.required_params + self.optional_params


with open(sys.argv[1]) as f:
    data = json.loads(f.read())


components = {}
component_namespaces: Mapping[str, ComponentNamespace] = {}


def load_component(openapi_name, openapi_def, component_namespace=None):
    if openapi_name == "$ref":
        return components[re.search("^#/components/schemas/(.+)$", openapi_def).group(1)]
    if tuple(openapi_def) == ("$ref",):
        return components[re.search("^#/components/schemas/(.+)$", openapi_def["$ref"]).group(1)]
    if openapi_name in components:
        return components[openapi_name]

    assert component_namespace is not None

    openapi_type = openapi_def["type"]
    properties = {}
    required_properties = []

    if openapi_type == "object":
        properties = {pname: load_component(pname, pdef, component_namespace=component_namespace) for pname, pdef in openapi_def.get("properties", {}).items()}

        additional_properties = openapi_def.get("additionalProperties", None)
        if isinstance(additional_properties, dict):
            if tuple(additional_properties) == ("$ref",):
                properties.update(load_component("$ref", additional_properties["$ref"]).properties)

        required_properties = openapi_def.get("required", [])

    elif openapi_type == "array":
        properties = {"items": load_component("items", openapi_def["items"], component_namespace=component_namespace)}

    comp = Component(
        openapi_name=openapi_name,
        openapi_type=openapi_type,
        component_namespace=component_namespace,
        properties=properties,
        required_properties=required_properties
    )
    component_namespaces.setdefault(component_namespace, ComponentNamespace(component_namespace)).components.append(comp)
    return comp


for openapi_name, openapi_def in data["components"]["schemas"].items():
    print(f"Loading component {openapi_name!r}")
    components[openapi_name] = load_component(openapi_name, openapi_def, component_namespace=openapi_name)


apis = {}
for path, path_def in data["paths"].items():
    for method, method_def in path_def.items():
        name = camel_to_snake(method_def["operationId"])
        #print(f"Loading API {name!r}")

        path_params = []
        query_params = []

        for param_def in method_def["parameters"]:

            if "$ref" in param_def:
                merge_def = data
                for key in param_def["$ref"].lstrip("#/").split("/"):
                    merge_def = merge_def[key]
                for key, val in merge_def.items():
                    param_def.setdefault(key, val)

            param_name = param_def["name"]

            param = APIParameter(
                name=to_python_param(param_name),
                openapi_type=param_def["schema"]["type"],
                required=param_def.get("required", True),
                description=param_def.get("description", None),
                wire_name=param_name
            )
            if param_def["in"] == "path":
                path_params.append(param)
            elif param_def["in"] == "query":
                query_params.append(param)

        doc_url=None
        match = re.search(r"\((https://[^\)]+)\)", method_def.get("description", ""))
        if match:
            doc_url = match.group(1)

        # Get the 200 response
        try:
            resp_ref = method_def["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
            response_class = re.search("^#/components/schemas/(.+)$", resp_ref).group(1).title().replace("_", "")
        except (KeyError, AttributeError):
            response_class = "JSONResponse"

        apis[name] = API(
            name=name,
            method=method.upper(),
            path_parts=[x for x in path.split("/") if x],
            path_params=path_params,
            query_params=query_params,
            description=method_def.get("summary", ""),
            doc_url=doc_url,
            has_body="requestBody" in method_def,
            response_class=response_class
        )

        print(env.get_template("api").render(api=apis[name]))


for k, v in sorted(component_namespaces.items()):
    data = v.to_python()
    if data:
        with open(f"workplace_search/_components/{k}.py", "w+") as f:
            f.truncate()
            f.write("\n".join(data))
