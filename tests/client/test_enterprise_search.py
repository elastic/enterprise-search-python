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

from elastic_enterprise_search import AppSearch, EnterpriseSearch, WorkplaceSearch
from tests.conftest import DummyNode


def test_sub_clients():
    client = EnterpriseSearch()
    assert isinstance(client.app_search, AppSearch)
    assert isinstance(client.workplace_search, WorkplaceSearch)

    # Requests Session is shared for pooling
    assert client.transport is client.app_search.transport
    assert client.transport is client.workplace_search.transport


def test_sub_client_auth():
    client = EnterpriseSearch(node_class=DummyNode, meta_header=False)

    # Using options on individual clients
    client.options(bearer_auth="enterprise-search").perform_request(
        "GET", "/enterprise-search"
    )
    client.app_search.options(bearer_auth="app-search").perform_request(
        "GET", "/app-search"
    )
    client.workplace_search.options(bearer_auth="workplace-search").perform_request(
        "GET", "/workplace-search"
    )

    # Authenticating doesn't modify other clients
    client.options(bearer_auth="not-app-search").app_search.perform_request(
        "GET", "/not-app-search"
    )
    client.options(bearer_auth="not-workplace-search").workplace_search.perform_request(
        "GET", "/not-workplace-search"
    )

    # The Authorziation header gets hidden
    calls = client.transport.node_pool.get().calls
    headers = [
        (target, kwargs["headers"].get("Authorization", None))
        for ((_, target), kwargs) in calls
    ]

    assert headers == [
        ("/enterprise-search", "Bearer enterprise-search"),
        ("/app-search", "Bearer app-search"),
        ("/workplace-search", "Bearer workplace-search"),
        ("/not-app-search", None),
        ("/not-workplace-search", None),
    ]
