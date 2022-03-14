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

import datetime

import pytest
from dateutil import tz

from elastic_enterprise_search import _utils


def test_format_datetime_tz_naive():
    dt = datetime.datetime.now()
    assert dt.tzinfo is None

    # Should serialize the same as local timezone
    dt2 = dt.replace(tzinfo=tz.tzlocal())

    assert _utils.format_datetime(dt) == _utils.format_datetime(dt2)

    # This is the dicey one, utcnow() is very broken and not recommended.
    dt = datetime.datetime.utcnow()
    assert dt.tzinfo is None

    dt2 = datetime.datetime.now(tz=tz.UTC)

    # The two are only equal if the local timezone is UTC
    # otherwise they are different :(
    if tz.tzlocal() == tz.UTC:
        assert _utils.format_datetime(dt) == _utils.format_datetime(dt2)
    else:
        assert _utils.format_datetime(dt) != _utils.format_datetime(dt2)


def test_to_params():
    params = [
        ("a", 1),
        ("b", "z"),
        ("c", ["d", 2]),
        ("e", datetime.date(year=2020, month=1, day=1)),
        (
            "f",
            datetime.datetime(
                year=2020,
                month=2,
                day=3,
                hour=4,
                minute=5,
                second=6,
                microsecond=7,
                tzinfo=tz.gettz("HST"),
            ),
        ),
        ("g", (True, False)),
        ("h", b"hello-world"),
        ("i", None),
        ("z", "[]1234567890-_~. `=!@#$%^&*()+;'{}:,<>?/\\\""),
        ("kv", {"key": [1, "2", {"k": "v"}]}),
    ]
    assert _utils._quote_query(params) == (
        "a=1&"
        "b=z&"
        "c[]=d&"
        "c[]=2&"
        "e=2020-01-01&"
        "f=2020-02-03T04:05:06.000007-10:00&"
        "g[]=True&g[]=False&"
        "h=hello-world&"
        "i=None&"
        "z=[]1234567890-_~.%20%60%3D%21%40%23%24%25%5E%26*%28%29%2B%3B%27%7B%7D:,%3C%3E%3F%2F%5C%22&"
        "kv[key][]=1&kv[key][]=2&kv[key][][k]=v"
    )


@pytest.mark.parametrize(
    ["value", "dt"],
    [
        (
            "2020-01-02T03:04:05Z",
            datetime.datetime(
                year=2020, month=1, day=2, hour=3, minute=4, second=5, tzinfo=tz.UTC
            ),
        ),
        (
            "2020-01-02T11:12:59+00:00",
            datetime.datetime(
                year=2020, month=1, day=2, hour=11, minute=12, second=59, tzinfo=tz.UTC
            ),
        ),
        (
            # An odd case of '-00:00' but we handle it anyways.
            "2020-01-02T11:12:59-00:00",
            datetime.datetime(
                year=2020, month=1, day=2, hour=11, minute=12, second=59, tzinfo=tz.UTC
            ),
        ),
        (
            "2020-01-02 11:12:59-10:00",
            datetime.datetime(
                year=2020,
                month=1,
                day=2,
                hour=11,
                minute=12,
                second=59,
                tzinfo=tz.gettz("HST"),
            ),
        ),
        (
            # 'Asia/Kolkata' is Indian Standard Time which is UTC+5:30 and doesn't have DST
            "2020-01-02T11:12:59+05:30",
            datetime.datetime(
                year=2020,
                month=1,
                day=2,
                hour=11,
                minute=12,
                second=59,
                tzinfo=tz.gettz("Asia/Kolkata"),
            ),
        ),
    ],
)
def test_parse_datetime(value, dt):
    assert _utils.parse_datetime(value) == dt


def test_parse_datetime_bad_format():
    with pytest.raises(ValueError) as e:
        _utils.parse_datetime("2020-03-10T10:10:10")
    assert (
        str(e.value)
        == "Datetime must match format '(YYYY)-(MM)-(DD)T(HH):(MM):(SS)(TZ)' was '2020-03-10T10:10:10'"
    )
