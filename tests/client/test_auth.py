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

import warnings

import pytest
from elastic_transport.client_utils import DEFAULT

from elastic_enterprise_search import EnterpriseSearch, WorkplaceSearch
from tests.conftest import DummyNode


def test_http_auth_none(client_class):
    client = client_class(node_class=DummyNode, meta_header=False)
    client.perform_request("GET", "/")

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1 and "Authorization" not in calls[-1][1]["headers"]

    client = client_class(http_auth=None, node_class=DummyNode, meta_header=False)
    client.perform_request("GET", "/")
    assert len(calls) == 1 and "Authorization" not in calls[-1][1]["headers"]


@pytest.mark.parametrize(
    ["auth_kwarg", "auth_value", "header_value"],
    [
        ("http_auth", ("user", "password"), "Basic dXNlcjpwYXNzd29yZA=="),
        ("http_auth", ("üser", "pӓssword"), "Basic w7xzZXI6cNOTc3N3b3Jk"),
        ("http_auth", "this-is-a-token", "Bearer this-is-a-token"),
        ("basic_auth", ("user", "password"), "Basic dXNlcjpwYXNzd29yZA=="),
        ("basic_auth", ("üser", "pӓssword"), "Basic w7xzZXI6cNOTc3N3b3Jk"),
        ("bearer_auth", "this-is-a-token", "Bearer this-is-a-token"),
    ],
)
def test_http_auth_set_and_get(client_class, auth_kwarg, auth_value, header_value):
    client = client_class(node_class=DummyNode, **{auth_kwarg: auth_value})
    client.perform_request("GET", "/")

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[-1][1]["headers"]["Authorization"] == header_value


def test_http_auth_per_request_override():
    client = EnterpriseSearch(http_auth="bad-token", node_class=DummyNode)
    with warnings.catch_warnings(record=True) as w:
        client.get_version(http_auth=("user", "password"))

    assert len(w) == 1 and str(w[0].message) == (
        "Passing transport options in the API method is deprecated. "
        "Use 'EnterpriseSearch.options()' instead."
    )

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[-1][1]["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="


def test_http_auth_disable_with_none():
    client = EnterpriseSearch(bearer_auth="api-token", node_class=DummyNode)
    client.perform_request("GET", "/")

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[-1][1]["headers"]["Authorization"] == "Bearer api-token"

    client.options(bearer_auth=None).get_version()
    assert len(calls) == 2
    assert "Authorization" not in calls[-1][1]["headers"]

    client.options(basic_auth=None).get_version()
    assert len(calls) == 3
    assert "Authorization" not in calls[-1][1]["headers"]


@pytest.mark.parametrize("http_auth", ["token", ("user", "pass")])
def test_auth_not_sent_with_oauth_exchange(http_auth):
    client = WorkplaceSearch(
        node_class=DummyNode, meta_header=False, http_auth=http_auth
    )
    client.oauth_exchange_for_access_token(
        client_id="client-id",
        client_secret="client-secret",
        redirect_uri="redirect-uri",
        code="code",
    )

    calls = client.transport.node_pool.get().calls
    assert calls == [
        (
            (
                "POST",
                "/ws/oauth/token?grant_type=authorization_code&client_id=client-id&client_secret=client-secret&redirect_uri=redirect-uri&code=code",
            ),
            {
                "body": None,
                "headers": {},
                "request_timeout": DEFAULT,
            },
        )
    ]
