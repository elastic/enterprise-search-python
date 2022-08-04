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

import pytest
from elastic_transport.client_utils import DEFAULT

from elastic_enterprise_search import AppSearch
from tests.conftest import DummyNode


def test_search_es_search():
    client = AppSearch(node_class=DummyNode, meta_header=False)
    client.search_es_search(
        engine_name="test",
        params={"key": "val"},
        body={"k": ["v", 2]},
        analytics_query="analytics-query",
    )

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[-1][1].pop("request_timeout") is DEFAULT
    assert calls[-1] == (
        (
            "POST",
            "/api/as/v0/engines/test/elasticsearch/_search?key=val",
        ),
        {
            "body": b'{"k":["v",2]}',
            "headers": {
                "accept": "application/json",
                "content-type": "application/json",
                "x-enterprise-search-analytics": "analytics-query",
            },
        },
    )


@pytest.mark.parametrize("analytics_tags", ["a,b", ["a", "b"]])
def test_analytics_tags(analytics_tags):
    client = AppSearch(node_class=DummyNode, meta_header=False)
    client.options(headers={"Extra": "value"}).search_es_search(
        engine_name="test", analytics_tags=analytics_tags
    )

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[-1][1].pop("request_timeout") is DEFAULT
    assert calls[-1] == (
        (
            "POST",
            "/api/as/v0/engines/test/elasticsearch/_search",
        ),
        {
            "body": None,
            "headers": {
                "extra": "value",
                "accept": "application/json",
                "content-type": "application/json",
                "x-enterprise-search-analytics-tags": "a,b",
            },
        },
    )


@pytest.mark.parametrize("param_value", [object(), 1, 2.0, (), [3]])
def test_search_es_search_params_type_error(param_value):
    client = AppSearch(node_class=DummyNode)

    with pytest.raises(TypeError) as e:
        client.search_es_search(
            engine_name="test",
            params={"key": param_value},
        )
    assert str(e.value) == "Values for 'params' parameter must be of type 'str'"
