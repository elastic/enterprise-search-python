#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import json
import os
import pathlib
import re
from functools import lru_cache
from typing import List, Optional

import jinja2
import urllib3

http = urllib3.PoolManager()
current_branch = "master"
base_dir = pathlib.Path(__file__).absolute().parent.parent.parent
schemas_dir = base_dir.parent / "ent-search/swagger/v1"
templates_dir = str(pathlib.Path(__file__).absolute().parent / "templates")
loader = jinja2.FileSystemLoader(templates_dir)
env = jinja2.Environment(
    loader=loader,
)
t = env.get_template("component")


http_status_errors = {
    400: "elastic_enterprise_search.BadRequestError",
    401: "elastic_enterprise_search.UnauthorizedError",
    402: "elastic_enterprise_search.PaymentRequiredError",
    403: "elastic_enterprise_search.ForbiddenError",
    404: "elastic_enterprise_search.NotFoundError",
    409: "elastic_enterprise_search.ConflictError",
    413: "elastic_enterprise_search.PayloadTooLargeError",
}


@lru_cache()
def is_valid_url(url):
    return 200 <= http.request("HEAD", url).status < 400


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
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name.replace("-", "_"))
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def snake_to_camel(name):
    if "_" in name:
        return "".join(x.title() for x in name.split("_"))
    return name[0].upper() + name[1:]


def to_python_param(name):
    return re.sub(r"[^a-z0-9_]+", "_", camel_to_snake(name)).strip("_")


class Parameter:
    def __init__(self, spec):
        self.spec = spec

    @property
    def wire_name(self):
        wire_name = self.spec["name"]

        # If there's an unstyled array with explode=True (or default 'True')
        # then we add '[]' after the spec wire name to comply with Ruby on Rails
        # query parameter arrays.
        if (
            self.type == "array"
            and self.style in (None, "form")
            and self.explode
            and not wire_name.endswith("[]")
        ):
            wire_name += "[]"

        return wire_name

    @property
    def param_name(self) -> str:
        return to_python_param(self.spec.get("x-codegen-param-name", self.spec["name"]))

    @property
    def required(self) -> bool:
        return self.spec.get("required", False)

    @property
    def in_(self) -> str:
        return self.spec.get("in", None)

    @property
    def description(self):
        return self.spec.get("description", "")

    @property
    def type(self):
        return self.spec.get("type", self.spec.get("schema", {}).get("type", None))

    @property
    def style(self):
        return self.spec.get("style", None)

    @property
    def explode(self):
        explode = self.spec.get("explode", None)
        if self.type == "array" and self.style is None and explode is None:
            return True  # By default we explode with x[]=...,x[]=...
        return explode

    def __repr__(self):
        return f"Parameter(param_name={self.param_name!r})"


class Component:
    def __init__(self, id, spec):
        self.id = id
        self.spec = spec

    @property
    def properties(self):
        return

    @property
    def class_name(self) -> str:
        return snake_to_camel(self.id)

    @property
    def typing_type(self):
        openapi_type = self.spec["type"]
        t = openapi_type_to_typing(openapi_type)
        if t:
            return t
        elif openapi_type == "array":
            return f"typing.List[{self.properties['items'].typing_type}]"
        else:
            return self.class_name

    def __repr__(self):
        return f"{self.class_name}()"


class API:
    def __init__(self, method, path, spec):
        self.method = method.upper()
        self.path = path
        self.spec = spec

    @staticmethod
    def sorted_key(api):
        func_parts = api.func_name.split("_")
        if func_parts[0] in (
            "get",
            "put",
            "update",
            "delete",
            "create",
            "add",
            "delete",
            "list",
            "reset",
            "index",
        ):
            if func_parts[1] == "all":
                return tuple(func_parts[2:] + func_parts[:2])
            return tuple(func_parts[1:] + func_parts[:1])
        return tuple(func_parts)

    @property
    def func_name(self) -> str:
        return camel_to_snake(self.spec["operationId"])

    @property
    def all_params(self):
        param_specs = self.spec.get("parameters", [])
        return sorted(
            [Parameter(spec) for spec in param_specs],
            key=lambda x: (not x.required, x.in_ == "query"),
        )

    @property
    def required_params(self):
        return [param for param in self.all_params if param.required]

    @property
    def optional_params(self):
        return [param for param in self.all_params if not param.required]

    @property
    def query_params(self):
        return [param for param in self.all_params if param.in_ == "query"]

    @property
    def path_parts(self):
        return [x for x in self.path.split("/") if x]

    @property
    def has_path_params(self):
        return any(part.startswith("{") for part in self.path_parts)

    @property
    def description(self) -> str:
        summary = self.spec["summary"]
        return summary[0].upper() + summary[1:]

    @property
    def docs_url(self) -> Optional[str]:
        url = self.spec.get("externalDocs", {}).get("url", None)
        if url is None:
            match = re.match(r"\[[^]]+?\]\(([^)]+)\)", self.spec.get("description", ""))
            if match:
                url = match.group(1)
        if url:
            new_url = re.sub(
                r"/guide/en/([a-z\-]+)/current/",
                r"/guide/en/\1/%s/" % current_branch,
                url,
            )
            if is_valid_url(new_url):
                url = new_url
        return url

    @property
    def raises(self) -> List[str]:
        errors = {}
        for http_status in self.spec.get("responses", {}).keys():
            if http_status == "default":
                continue
            http_status = int(http_status)
            if (
                http_status >= 300 and http_status in http_status_errors
            ):  # Don't raise on 2XX
                errors[http_status] = http_status_errors[http_status]
        return [v for k, v in sorted(errors.items())]

    @property
    def has_body(self) -> bool:
        return "requestBody" in self.spec

    @property
    def body_param_name(self) -> str:
        return to_python_param(self.spec.get("x-codegen-request-body-name", "body"))

    @property
    def body_required(self) -> bool:
        # TODO: OpenAPI actually should default to 'False' but
        # the Enterprise Search specs seem to default to 'True' so
        # for now we do this.
        return self.spec.get("requestBody", {}).get("required", True)

    @property
    def body_description(self):
        if self.has_body:
            return self.spec["requestBody"].get("description", "HTTP request body")
        return None

    @property
    def response_component(self) -> str:
        spec_resps = self.spec["responses"]
        resp = spec_resps.get("default", spec_resps.get("200", ""))
        ref = None
        if "$ref" in resp:
            ref = resp["$ref"]
        elif "content" in resp:
            ref = resp["content"]["application/json"]["schema"]["$ref"]
        if ref:
            return re.match(
                r"^#/?components/(?:schemas|responses|requestBodies)/(.+)$", ref
            ).group(1)

    @property
    def asciidoc_fragment(self) -> str:
        return re.sub(r"[^a-zA-Z0-9]+", "-", self.func_name).strip("-")

    def __repr__(self):
        return f"API(func_name={self.func_name!r}, method={self.method!r}, path={self.path!r}, resp={self.response_component!r})"


class OpenAPI:
    def __init__(self, namespace, components, apis):
        self.namespace = namespace
        self.components = components
        self.apis = [self.process_api(api) for api in apis]

    @property
    def client_class_name(self):
        return snake_to_camel(self.namespace)

    def process_api(self, api):
        # type: (API) -> API
        """Called once per API to do final processing if any"""

        # app_search.multi_search() has the 'queries' parameter in the URL query
        # when it should be in the body due to it's size and complexity.
        # Updating this here so it's available in 7.11:
        if (
            current_branch == "7.11"
            and self.namespace == "_app_search"
            and api.func_name == "multi_search"
        ):
            # Remove 'queries' parameter, add a 'requestBody' parameter
            api.spec["requestBody"] = {
                "required": True,
                "description": "One or more queries to execute in parallel",
            }
            api.spec["parameters"] = [
                param for param in api.spec["parameters"] if param["name"] != "queries"
            ]

        return api

    @classmethod
    def from_schema(cls, filepath: pathlib.Path):
        with filepath.open() as f:
            schema_data = json.loads(f.read())

        def expand_refs(x):
            if isinstance(x, list):
                return [expand_refs(i) for i in x]
            elif isinstance(x, dict):
                if "$ref" in x or ("schema" in x and tuple(x["schema"]) == ("$ref",)):
                    keys = (
                        re.match(
                            r"^#/?(.*)$",
                            x["$ref"] if "$ref" in x else x["schema"]["$ref"],
                        )
                        .group(1)
                        .split("/")
                    )
                    base = schema_data
                    for key in keys:
                        base = base[key]
                    base = base.copy()
                    x.pop("$ref" if "$ref" in x else "schema")
                    base.update(x)
                    return base
                else:
                    return {k: expand_refs(v) for k, v in x.items()}
            return x

        schema_data = expand_refs(schema_data)
        namespace = "_" + filepath.name.replace(".json", "").replace("-", "_")
        apis = []
        components = {}
        for cat, cat_val in schema_data.get("components", {}).items():
            for name, spec in cat_val.items():
                components[name] = Component(name, spec)
        for path_key, path_val in schema_data["paths"].items():
            path_parameters = []
            for method_key, method_val in path_val.items():
                if method_key == "parameters":
                    path_parameters.extend(method_val)
                    continue
                apis.append(API(method=method_key, path=path_key, spec=method_val))
            for api in apis:
                if api.path == path_key:
                    api.spec.setdefault("parameters", []).extend(path_parameters)

        apis = sorted(apis, key=API.sorted_key)
        return OpenAPI(namespace, components=components, apis=apis)

    def __repr__(self):
        return (
            f"OpenAPI(\n"
            f"  namespace={self.namespace!r},\n"
            f"  components={self.components},\n"
            f"  apis={self.apis}\n"
            f")"
        )


def main():
    specs = []
    for filepath in schemas_dir.iterdir():
        specs.append(OpenAPI.from_schema(filepath))

    for spec in specs:
        spec_filepath = (
            base_dir / f"elastic_enterprise_search/client/{spec.namespace}.py"
        )
        with spec_filepath.open(mode="w") as f:
            f.truncate()
            f.write(env.get_template("client").render(spec=spec))

    os.system(f"cd {base_dir} && nox -rs format")


if __name__ == "__main__":
    main()
