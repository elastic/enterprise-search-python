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
from six import ensure_str, ensure_binary, ensure_text
from dateutil import tz

SKIP_IN_PATH = (None, "", b"", [], ())
PY2 = sys.version_info[0] == 2

if PY2:
    string_types = (basestring,)  # noqa: F821
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

__all__ = ["typing", "escape", "make_path", "make_params", "PY2", "BaseClient"]


class BaseClient(object):
    def __init__(
        self,
        _transport=None,
        transport_class=None,
        host=None,
        port=None,
        use_ssl=None,
        verify_certs=None,
        ca_certs=None,
        **kwargs
    ):
        http_auth = kwargs.pop("http_auth", None)
        kwargs.update(
            {
                "host": host,
                "port": port,
                "use_ssl": use_ssl,
                "verify_certs": verify_certs,
                "ca_certs": ca_certs,
            }
        )
        if _transport is not None:
            if transport_class is not None or any(
                v is not None for v in kwargs.values()
            ):
                raise ValueError(
                    "Can't pass both a Transport and parameters to a client"
                )
            self.transport = _transport
        else:
            self.transport = (transport_class or Transport)(**kwargs)
        if http_auth:
            self.http_auth = http_auth

    def authenticate(self, http_auth):
        """Create a new client with different authentication. This is useful
        when authenticating with a users access token as the HTTP transport
        is re-used rather than being newly created each time.

        :arg http_auth: Either a (username, password) tuple for 'Basic'
            auth or a string for 'Bearer' token auth.
        """
        transport = self.transport.copy()
        return type(self)(_transport=transport, http_auth=http_auth)

    @property
    def http_auth(self):
        auth_header = self.transport.headers.get("authorization", None)
        if auth_header:
            # We split basic auth into a tuple if we can
            if auth_header.startswith("Basic "):
                try:
                    b64_encoded = ensure_binary(auth_header.partition(" ")[-1])
                    b64_decoded = ensure_text(base64.b64decode(b64_encoded))
                    return tuple(b64_decoded.split(":", 1))
                except Exception as e:
                    print(e)
            return auth_header.partition(" ")[-1]
        return None

    @http_auth.setter
    def http_auth(self, http_auth):
        # Basic auth with (username, password)
        if isinstance(http_auth, (tuple, list)) and len(http_auth) == 2:
            basic_auth = ensure_str(
                base64.b64encode((b":".join([ensure_binary(x) for x in http_auth])))
            )
            self.transport.headers["authorization"] = "Basic %s" % basic_auth

        # If not a tuple/list or string raise an error.
        elif not isinstance(http_auth, str):
            raise TypeError(
                "'http_auth' must either be a tuple of (username, password) "
                "for 'Basic' authentication or a single string for "
                "'Bearer'/token authentication"
            )

        # Bearer / Token auth
        else:
            self.transport.headers["authorization"] = "Bearer %s" % http_auth


def escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = b",".join([escape(x) for x in value])

    # Convert datetimes timezone info to
    # UTC and then format to RFC 3339
    elif isinstance(value, datetime):
        # If there's timezone information defined then convert to UTC.
        # If it's a naive datetime assume local time.
        if value.tzinfo is None:
            value = value.astimezone(tz.tzlocal())
        return value.astimezone(tz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    elif isinstance(value, date):
        return value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    if not isinstance(value, string_types):
        value = str(value)

    return ensure_binary(value)


def make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    return "/" + "/".join(
        # preserve ',' and '*' in url for nicer URLs in logs
        quote(escape(p), b",*[]:-")
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
    wire_params = {
        k: quote(escape(v), b",*[]:-")
        for k, v in (extra_params or {}).items()
        if v is not None
    }
    if set(wire_params).intersection(set(params)):
        raise ValueError("Conflict between keyword argument and 'params'")
    for k, v in (params or {}).items():
        if v is None:
            continue
        wire_params[k] = quote(escape(v), b",*[]:-")
    return wire_params
