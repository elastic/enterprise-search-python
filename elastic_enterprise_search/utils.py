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

import sys
from datetime import date, datetime
from six import ensure_binary
from six.moves.urllib_parse import urlencode, urlparse, unquote, quote
from dateutil import tz

__all__ = [
    "urlparse",
    "urlencode",
    "unquote",
    "string_types",
    "escape",
    "make_path",
    "make_params",
    "PY2",
    "SKIP_IN_PATH",
]

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


def escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = b",".join([escape(x) for x in value])

    elif isinstance(value, datetime):
        value = format_datetime(value)

    elif isinstance(value, date):
        value = value.isoformat()

    # don't decode bytestrings
    elif isinstance(value, bytes):
        return value

    elif isinstance(value, bool):
        value = str(value).lower()

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


def format_datetime(value):
    """Convert datetimes timezone info to
    UTC and then format to RFC 3339
    """
    # If there's timezone information defined then convert to UTC.
    # If it's a naive datetime assume local time.
    if value.tzinfo is None:
        value = value.astimezone(tz.tzlocal())
    return value.astimezone(tz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
