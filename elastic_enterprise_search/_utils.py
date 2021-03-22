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

import re
import sys
from datetime import date, datetime

from dateutil import parser, tz
from elastic_transport import QueryParams  # noqa: F401
from elastic_transport.compat import Mapping, quote, urlencode, urlparse
from elastic_transport.utils import DEFAULT as DEFAULT
from six import ensure_str

__all__ = [
    "DEFAULT",
    "PY2",
    "SKIP_IN_PATH",
    "default_params_encoder",
    "format_datetime",
    "parse_datetime",
    "string_types",
    "to_array",
    "to_deep_object",
    "to_path",
    "typing",
    "urlencode",
    "urlparse",
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


def to_param(value):
    # type: (typing.Any) -> str
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.

    Note that 'exploded' query string arrays are converted to individual key-value
    pairs first so won't be encoded as a list/tuple by this method.
    """
    if isinstance(value, (list, tuple)):
        value = ",".join([to_param(val) for val in value])

    elif isinstance(value, datetime):
        value = format_datetime(value)

    elif isinstance(value, date):
        value = value.isoformat()

    elif isinstance(value, bytes):
        value = ensure_str(value, encoding="utf-8", errors="surrogatepass")

    elif isinstance(value, bool):
        value = str(value).lower()

    if not isinstance(value, string_types):
        value = str(value)
    return value


def to_path(*parts):
    # type: (typing.Any) -> str
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    return "/" + "/".join(
        # Don't percent encode these characters for nicer logs
        quote(to_param(part), ",*[]:-")
        for part in parts
        if part not in SKIP_IN_PATH
    )


def to_array(value, param=None):
    # type: (typing.Union[typing.Tuple[typing.Any, ...], typing.List[typing.Any]], str) -> typing.Sequence[typing.Any]
    """Ensures that a parameter is an array"""
    if not isinstance(value, (tuple, list)):
        raise TypeError(
            "Parameter %smust be a tuple or list"
            % (repr(param) + " " if param else "",)
        )
    return value


def to_deep_object(param, value):
    # type: (str, typing.Mapping[str, typing.Any]) -> typing.Sequence[typing.Tuple[str, str]]
    """Converts a complex object into query parameter key values"""
    if not isinstance(value, Mapping):
        raise TypeError("Parameter %r must be a mapping" % (param,))

    def inner(prefix, obj):
        if isinstance(obj, Mapping):
            for key, val in obj.items():
                for ret in inner("%s[%s]" % (prefix, key), val):
                    yield ret

        elif isinstance(obj, (tuple, list)):
            for item in obj:
                for ret in inner(prefix + "[]", item):
                    yield ret
        else:
            yield prefix, to_param(obj)

    return list(inner(param, value))


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
        timezone = "{}{:02}:{:02}".format(offset_sign, hours, minutes)
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


def default_params_encoder(params):
    # type: (QueryParams) -> str
    """Convert a elastic_transport.QueryParams instance
    into the query section of a URL.

    This function is used for elastic_transport.Transport(params_encoder)
    """
    to_encode = []
    for key, val in params.items():
        key = quote(key, ",*[]:-")
        if val is not None:  # pass-through None values
            val = quote(to_param(val), ",*[]:-")
        to_encode.append((key, val))
    return "&".join(
        ("%s=%s" % (key, val) if val is not None else key) for key, val in to_encode
    )
