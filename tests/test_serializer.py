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

from elastic_enterprise_search import JSONSerializer


def test_serializer_formatting():
    serializer = JSONSerializer()
    assert (
        serializer.dumps(
            {
                "d": datetime.datetime(
                    year=2020,
                    month=12,
                    day=11,
                    hour=10,
                    minute=9,
                    second=8,
                    tzinfo=tz.UTC,
                ),
            }
        )
        == '{"d":"2020-12-11T10:09:08Z"}'
    )
    assert (
        serializer.dumps({"t": datetime.date(year=2020, month=1, day=29)})
        == '{"t":"2020-01-29"}'
    )
