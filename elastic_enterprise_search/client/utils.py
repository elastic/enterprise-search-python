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
import sys
from datetime import date, datetime
from ..transport import Transport
from six import b

SKIP_IN_PATH = (None, "", b"", [], ())
PY2 = sys.version_info[0] == 2

if PY2:
    string_types = (basestring,)
else:
    string_types = (str, bytes)

try:
    import typing
except ImportError:
    typing = None

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

__all__ = ["typing", "escape", "make_path", "PY2", "BaseClient", "JSONResponse"]


class BaseClient(object):
    def __init__(self, _transport=None, transport_class=None, **kwargs):
        if _transport is not None:
            if transport_class is not None or kwargs:
                raise ValueError(
                    "Can't pass both a Transport and parameters to a client"
                )
            self.transport = _transport
        else:
            http_auth = kwargs.pop("http_auth", None)
            self.transport = (transport_class or Transport)(**kwargs)
            if http_auth:
                self.http_auth = http_auth

    @property
    def http_auth(self):
        auth_header = self.transport.headers.get("authorization", None)
        if auth_header:
            return auth_header.replace("Bearer ", "", 1)
        return None

    @http_auth.setter
    def http_auth(self, auth_token):
        # Basic auth with (username, password)
        if isinstance(auth_token, (tuple, list)) and len(auth_token) == 2:
            basic_auth = base64.b64encode(b(":".join(auth_token))).decode()
            self.transport.headers["authorization"] = "Basic %s" % basic_auth

        # If not a tuple/list or string raise an error.
        elif not isinstance(auth_token, str):
            raise TypeError(
                "'http_auth' must either be a tuple of (username, password) "
                "for 'Basic' authentication or a single string for "
                "'Bearer'/token authentication"
            )

        # Bearer / Token auth
        else:
            self.transport.headers["authorization"] = "Bearer %s" % auth_token


class JSONResponse(dict):
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        super(JSONResponse, self).__init__(body)


def escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = ",".join(value)

    # dates and datetimes into isoformat
    elif isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    # encode strings to utf-8
    if isinstance(value, string_types):
        if PY2 and isinstance(value, unicode):  # noqa: F821
            return value.encode("utf-8")
        if not PY2 and isinstance(value, str):
            return value.encode("utf-8")

    return str(value)


def make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    return "/" + "/".join(
        # preserve ',' and '*' in url for nicer URLs in logs
        quote(escape(p), b",*")
        for p in parts
        if p not in SKIP_IN_PATH
    )


def make_params(params, extra_params):
    """
    Creates URL query params by combining arbitrary params
    with params designated by keyword arguments and escapes
    them to be compatible with HTTP request URI.

    Raises an exception if there is a conflict between the
    two ways to specify a query param.
    """
    params = params or {}
    wire_params = {k: quote(escape(v), b",*") for k, v in (extra_params or {}).items()}
    if set(wire_params).intersection(set(params)):
        raise ValueError("Conflict between key-word argument and 'params'")
    for k, v in (params or {}).items():
        wire_params[k] = quote(escape(v), b",*")
    return wire_params
