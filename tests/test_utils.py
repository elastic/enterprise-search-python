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
from dateutil import tz
from elastic_enterprise_search.client import utils


def test_make_params():
    assert utils.make_params(
        {},
        {
            "a": 1,
            "b": "z",
            "c": ["d", 2],
            "e": datetime.date(year=2020, month=1, day=1),
            "f": datetime.datetime(
                year=2020,
                month=2,
                day=3,
                hour=4,
                minute=5,
                second=6,
                microsecond=7,
                tzinfo=tz.gettz("HST"),
            ),
            "g": True,
        },
    ) == {
        "a": "1",
        "b": "z",
        "c": "d,2",
        "e": "2020-01-01",
        "f": "2020-02-03T14:05:06Z",
        "g": "true",
    }


def test_make_path():
    assert (
        utils.make_path(
            "a",
            1,
            "z",
            ["d", 2],
            datetime.date(year=2020, month=1, day=1),
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
            True,
        )
        == "/a/1/z/d,2/2020-01-01/2020-02-03T14:05:06Z/true"
    )


def test_datetime_with_timezone():
    # Hawaii Standard Time is UTC-10 and doesn't observe
    # daylight savings so this should continue to pass :)
    dt = datetime.datetime(
        year=2020, month=1, day=1, hour=10, minute=0, second=0, tzinfo=tz.gettz("HST")
    )

    assert utils.make_params({}, {"dt": dt}) == {"dt": "2020-01-01T20:00:00Z"}
