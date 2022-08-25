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

import base64
import inspect
import re
import sys
import typing as t
import warnings
from datetime import date, datetime
from functools import wraps
from pathlib import Path

from dateutil import parser, tz
from elastic_transport import HttpHeaders, NodeConfig
from elastic_transport.client_utils import (
    DEFAULT,
    DefaultType,
    client_meta_version,
    create_user_agent,
    percent_encode,
    url_to_node_config,
)

from ._version import __version__

__all__ = [
    "DEFAULT",
    "SKIP_IN_PATH",
    "format_datetime",
    "parse_datetime",
    "resolve_auth_headers",
]

F = t.TypeVar("F")
SKIP_IN_PATH = {None, "", b""}
CLIENT_META_SERVICE = ("ent", client_meta_version(__version__))
USER_AGENT = create_user_agent("enterprise-search-python", __version__)

_TRANSPORT_OPTIONS = {
    "http_auth",
    "request_timeout",
    "opaque_id",
    "headers",
    "ignore_status",
}


def format_datetime(value):
    # type: (datetime) -> str
    """Format a datetime object to RFC 3339"""
    # When given a timezone unaware datetime, use local timezone.
    if value.tzinfo is None:
        value = value.replace(tzinfo=tz.tzlocal())

    utcoffset = value.utcoffset()
    offset_secs = utcoffset.total_seconds()
    # Use 'Z' for UTC, otherwise use '[+-]XX:XX' for tz offset
    if offset_secs == 0:
        timezone = "Z"
    else:
        offset_sign = "+" if offset_secs >= 0 else "-"
        offset_secs = int(abs(offset_secs))
        hours = offset_secs // 3600
        minutes = (offset_secs % 3600) // 60
        timezone = f"{offset_sign}{hours:02}:{minutes:02}"
    return value.strftime("%Y-%m-%dT%H:%M:%S") + timezone


def parse_datetime(value):
    # type: (str) -> datetime
    """Convert a string value RFC 3339 into a datetime with tzinfo"""
    if not re.match(
        r"^[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+\-][0-9]{2}:[0-9]{2})$",
        value,
    ):
        raise ValueError(
            "Datetime must match format '(YYYY)-(MM)-(DD)T(HH):(MM):(SS)(TZ)' was '%s'"
            % value
        )
    return parser.isoparse(value)


def resolve_auth_headers(
    *,
    headers: t.Optional[t.Mapping[str, str]],
    http_auth: t.Union[DefaultType, None, t.Tuple[str, str], str] = DEFAULT,
    basic_auth: t.Union[DefaultType, None, t.Tuple[str, str], str] = DEFAULT,
    bearer_auth: t.Union[DefaultType, None, str] = DEFAULT,
) -> HttpHeaders:
    # Return an HttpHeaders instance. Can return values with 'None'
    # which are meant to be popped from an existing HttpHeaders instance
    # if two instances are being combined together.

    if headers is None or headers is DEFAULT:
        headers = HttpHeaders()
    elif not isinstance(headers, HttpHeaders):
        headers = HttpHeaders(headers)

    # Handle special authentication options
    auth_params_given = sum(
        x is not DEFAULT for x in (http_auth, basic_auth, bearer_auth)
    )
    if auth_params_given > 1:
        # More than one authentication parameter would have conflicts.
        # Don't allow users to specify both.
        raise ValueError(
            "Can't specify more than one authentication parameter (basic_auth/bearer_auth)"
        )

    # If there's exactly one parameter specified we can apply it to headers.
    if auth_params_given == 1:
        # http_auth -> bearer_auth / basic_auth
        if http_auth is not DEFAULT:
            if http_auth is None:
                basic_auth = None
            elif isinstance(http_auth, (list, tuple)) and all(
                isinstance(x, str) for x in http_auth
            ):
                basic_auth = http_auth
            elif isinstance(http_auth, str):
                bearer_auth = http_auth
            else:
                raise TypeError(
                    "The deprecated 'http_auth' parameter must be either 'Tuple[str, str]' or 'str'. "
                    "Use the 'basic_auth' or 'bearer_auth' parameters instead"
                )

            warnings.warn(
                "The 'http_auth' parameter is deprecated. "
                "Use 'basic_auth' or 'bearer_auth' parameters instead",
                category=DeprecationWarning,
                stacklevel=warn_stacklevel(),
            )

        # Setting the 'Authorization' header would be a conflict.
        if headers and headers.get("authorization", None) is not None:
            raise ValueError(
                "Can't set 'Authorization' HTTP header with other authentication options"
            )

        # Basic auth
        if isinstance(basic_auth, str):
            headers["authorization"] = f"Basic {basic_auth}"
        elif isinstance(basic_auth, (list, tuple)):
            headers[
                "authorization"
            ] = f"Basic {base64.b64encode(':'.join(basic_auth).encode('utf-8')).decode('ascii')}"
        elif basic_auth is None:
            headers["authorization"] = None
        elif basic_auth is not DEFAULT:
            raise TypeError(
                "'basic_auth' must be a string or 2 item list/tuple of strings"
            )

        # Bearer auth
        if isinstance(bearer_auth, str):
            headers["authorization"] = f"Bearer {bearer_auth}"
        elif bearer_auth is None:
            headers["authorization"] = None
        elif bearer_auth is not DEFAULT:
            raise TypeError("'bearer_auth' must be a string")

    return headers


def client_node_configs(hosts, **kwargs) -> t.List[NodeConfig]:
    if hosts is None or hosts is DEFAULT:
        hosts = ["http://localhost:3002"]
    if not isinstance(hosts, (list, tuple)):
        hosts = [hosts]
    node_configs = []
    for host in hosts:
        if isinstance(host, str):
            node_configs.append(
                url_to_node_config(host, use_default_ports_for_scheme=True)
            )
        else:
            raise TypeError("URLs must be of type 'str'")

    # Remove all values which are 'DEFAULT' to avoid overwriting actual defaults.
    node_options = {k: v for k, v in kwargs.items() if v is not DEFAULT}

    # Set the 'User-Agent' default header.
    headers = HttpHeaders(node_options.pop("headers", ()))
    headers.setdefault("user-agent", USER_AGENT)
    node_options["headers"] = headers

    def apply_node_options(node_config: NodeConfig) -> NodeConfig:
        """Needs special handling of headers since .replace() wipes out existing headers"""
        nonlocal node_options
        headers = node_config.headers.copy()  # type: ignore[attr-defined]

        headers_to_add = node_options.pop("headers", ())
        if headers_to_add:
            headers.update(headers_to_add)

        headers.setdefault("user-agent", USER_AGENT)
        headers.freeze()
        node_options["headers"] = headers
        return node_config.replace(**node_options)

    return [apply_node_options(node_config) for node_config in node_configs]


def warn_stacklevel() -> int:
    """Dynamically determine warning stacklevel for warnings based on the call stack"""
    try:
        # Grab the root module from the current module '__name__'
        module_name = __name__.partition(".")[0]
        module_path = Path(sys.modules[module_name].__file__)  # type: ignore[arg-type]

        # If the module is a folder we're looking at
        # subdirectories, otherwise we're looking for
        # an exact match.
        module_is_folder = module_path.name == "__init__.py"
        if module_is_folder:
            module_path = module_path.parent

        # Look through frames until we find a file that
        # isn't a part of our module, then return that stacklevel.
        for level, frame in enumerate(inspect.stack()):
            # Garbage collecting frames
            frame_filename = Path(frame.filename)
            del frame

            if (
                # If the module is a folder we look at subdirectory
                module_is_folder
                and module_path not in frame_filename.parents
            ) or (
                # Otherwise we're looking for an exact match.
                not module_is_folder
                and module_path != frame_filename
            ):
                return level
    except KeyError:
        pass
    return 0


def _escape(value: t.Any) -> str:
    """Escape a value into a string"""
    if isinstance(value, date):
        return value.isoformat()
    elif isinstance(value, datetime):
        return format_datetime(value)
    elif isinstance(value, bytes):
        return value.decode("utf-8", "surrogatepass")
    if not isinstance(value, str):
        return str(value)
    return value


def _quote(value: t.Any) -> str:
    """Percent-encode a value according to values that Enterprise Search accepts un-encoded"""
    return percent_encode(_escape(value), ",*[]:-")


def _quote_query(
    query: t.Union[t.Mapping[str, t.Any], t.Iterable[t.Tuple[str, t.Any]]]
) -> str:
    """Quote an iterable or mapping of key-value pairs into a querystring"""
    unquoted_kvs = query.items() if hasattr(query, "items") else query
    kvs: t.List[t.Tuple[str, str]] = []
    for k, v in unquoted_kvs:
        if isinstance(v, (list, tuple, dict)):
            if k.endswith("[]"):
                k = k[:-2]
            kvs.extend(_quote_query_deep_object(k, v))
        else:
            kvs.append((k, _quote(v)))

    return "&".join([f"{k}={v}" for k, v in kvs])


def _quote_query_deep_object(
    prefix: str, value: t.Any
) -> t.Iterable[t.Tuple[str, str]]:
    """Quote a list or mapping object into a querystring"""
    if not isinstance(value, (list, tuple, dict)):
        yield (prefix, _quote(value))
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _quote_query_deep_object(f"{prefix}[]", item)
    else:
        for key, val in value.items():
            yield from _quote_query_deep_object(f"{prefix}[{key}]", val)


def _quote_query_form(key: str, value: t.Union[t.List[str], t.Tuple[str, ...]]) -> str:
    if not isinstance(value, (tuple, list)):
        raise ValueError(f"{key!r} must be of type list or tuple")
    return ",".join(map(str, value))


def _merge_kwargs_no_duplicates(
    kwargs: t.Dict[str, t.Any], values: t.Dict[str, t.Any]
) -> None:
    for key, val in values.items():
        if key in kwargs:
            raise ValueError(
                f"Received multiple values for '{key}', specify parameters "
                "directly instead of using 'body' or 'params'"
            )
        kwargs[key] = val


def _rewrite_parameters(
    body_name: t.Optional[str] = None,
    body_fields: bool = False,
    parameter_aliases: t.Optional[t.Dict[str, str]] = None,
    ignore_deprecated_options: t.Optional[t.Set[str]] = None,
) -> t.Callable[[F], F]:
    def wrapper(api: F) -> F:
        @wraps(api)
        def wrapped(*args: t.Any, **kwargs: t.Any) -> t.Any:
            nonlocal api, body_name, body_fields

            # Let's give a nicer error message when users pass positional arguments.
            if len(args) >= 2:
                raise TypeError(
                    "Positional arguments can't be used with client API methods. "
                    "Instead only use keyword arguments."
                )

            # We merge 'params' first as transport options can be specified using params.
            if "params" in kwargs and (
                not ignore_deprecated_options
                or "params" not in ignore_deprecated_options
            ):
                params = kwargs.pop("params")
                if params:
                    if not hasattr(params, "items"):
                        raise ValueError(
                            "Couldn't merge 'params' with other parameters as it wasn't a mapping. "
                            "Instead of using 'params' use individual API parameters"
                        )
                    warnings.warn(
                        "The 'params' parameter is deprecated and will be removed "
                        "in a future version. Instead use individual parameters.",
                        category=DeprecationWarning,
                        stacklevel=warn_stacklevel(),
                    )
                    _merge_kwargs_no_duplicates(kwargs, params)

            maybe_transport_options = _TRANSPORT_OPTIONS.intersection(kwargs)
            if maybe_transport_options:
                transport_options = {}
                for option in maybe_transport_options:
                    if (
                        ignore_deprecated_options
                        and option in ignore_deprecated_options
                    ):
                        continue

                    # 'http_auth' needs to be aliased to 'basic_auth' or 'bearer_auth'.
                    transport_option = option
                    if option == "http_auth":
                        if isinstance(kwargs["http_auth"], str):
                            transport_option = "bearer_auth"
                        elif (
                            isinstance(kwargs["http_auth"], (list, tuple))
                            and len(kwargs["http_auth"]) == 2
                        ):
                            transport_option = "basic_auth"
                        else:
                            raise TypeError(
                                "'http_auth' must be either a str or a 2-tuple of strings"
                            )

                    try:
                        transport_options[transport_option] = kwargs.pop(option)
                    except KeyError:
                        pass

                if transport_options:
                    client = args[0].options(**transport_options)
                    warnings.warn(
                        "Passing transport options in the API method is deprecated. "
                        f"Use '{type(client).__name__}.options()' instead.",
                        category=DeprecationWarning,
                        stacklevel=warn_stacklevel(),
                    )
                    args = (client,) + args[1:]

            if "body" in kwargs and (
                not ignore_deprecated_options or "body" not in ignore_deprecated_options
            ):
                body = kwargs.pop("body")
                if body is not None:
                    if body_name:
                        if body_name in kwargs:
                            raise TypeError(
                                f"Can't use '{body_name}' and 'body' parameters together because '{body_name}' "
                                "is an alias for 'body'. Instead you should only use the "
                                f"'{body_name}' parameter."
                            )

                        warnings.warn(
                            "The 'body' parameter is deprecated and will be removed "
                            f"in a future version. Instead use the '{body_name}' parameter.",
                            category=DeprecationWarning,
                            stacklevel=warn_stacklevel(),
                        )
                        kwargs[body_name] = body

                    elif body_fields:
                        if not hasattr(body, "items"):
                            raise ValueError(
                                "Couldn't merge 'body' with other parameters as it wasn't a mapping. "
                                "Instead of using 'body' use individual API parameters"
                            )
                        warnings.warn(
                            "The 'body' parameter is deprecated and will be removed "
                            "in a future version. Instead use individual parameters.",
                            category=DeprecationWarning,
                            stacklevel=warn_stacklevel(),
                        )

                        # Special handling of page:{current:1,size:20} -> current_page=1, page_size=20
                        if "page" in body and set(body["page"]).issubset(
                            {"current", "size"}
                        ):
                            page = body.pop("page")
                            if "current" in page:
                                kwargs["current_page"] = page["current"]
                            if "size" in page:
                                kwargs["page_size"] = page["size"]

                        _merge_kwargs_no_duplicates(kwargs, body)

            if parameter_aliases:
                for alias, rename_to in parameter_aliases.items():
                    try:
                        kwargs[rename_to] = kwargs.pop(alias)
                    except KeyError:
                        pass

            return api(*args, **kwargs)

        return wrapped  # type: ignore[return-value]

    return wrapper
