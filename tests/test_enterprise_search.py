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

from elastic_enterprise_search import EnterpriseSearch, AppSearch, WorkplaceSearch


def test_sub_clients():
    client = EnterpriseSearch()
    assert isinstance(client.app_search, AppSearch)
    assert isinstance(client.workplace_search, WorkplaceSearch)

    # Requests Session is shared for pooling
    assert client.transport._session is client.app_search.transport._session
    assert client.transport._session is client.workplace_search.transport._session

    # Authenticating doesn't modify other clients
    client.http_auth = ("user", "pass")
    client.app_search.http_auth = "token-app-search"
    client.workplace_search.http_auth = "token-workplace-search"

    assert client.http_auth == ("user", "pass")
    assert client.app_search.http_auth == "token-app-search"
    assert client.workplace_search.http_auth == "token-workplace-search"

    assert client.transport.headers["authorization"] == "Basic dXNlcjpwYXNz"
    assert (
        client.app_search.transport.headers["authorization"]
        == "Bearer token-app-search"
    )
    assert (
        client.workplace_search.transport.headers["authorization"]
        == "Bearer token-workplace-search"
    )
