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

from elastic_enterprise_search import NotFoundError, WorkplaceSearch

access_token = "b6e5d30d7e5248533b5a8f5362e16853e2fc32826bc940aa32bf3ff1f1748f9b"
content_source_id = "5f7e1407678c1d8435a949a8"


@pytest.fixture()
def workplace_search():
    yield WorkplaceSearch("http://localhost:3002", http_auth=access_token)


@pytest.mark.vcr()
def test_index_documents(workplace_search):
    dt = datetime.datetime(year=2019, month=6, day=1, hour=12, tzinfo=tz.UTC)
    resp = workplace_search.index_documents(
        content_source_id=content_source_id,
        documents=[
            {
                "id": 1234,
                "title": "The Meaning of Time",
                "body": "Not much. It is a made up thing.",
                "url": "https://example.com/meaning/of/time",
                "created_at": dt,
            },
            {
                "id": 1235,
                "title": "The Meaning of Sleep",
                "body": "Rest, recharge, and connect to the Ether.",
                "url": "https://example.com/meaning/of/sleep",
                "created_at": dt,
            },
        ],
    )
    assert resp.status == 200
    assert resp == {
        "results": [{"id": "1234", "errors": []}, {"id": "1235", "errors": []}]
    }


@pytest.mark.vcr()
def test_index_documents_content_source_not_found(workplace_search):
    with pytest.raises(NotFoundError) as e:
        workplace_search.index_documents(
            content_source_id=content_source_id + "a",
            documents=[
                {
                    "id": 1234,
                    "title": "The Meaning of Time",
                },
            ],
        )
    assert e.value.status == 404
    assert e.value.message == ""
