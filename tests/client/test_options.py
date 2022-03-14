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

import inspect

import pytest

from elastic_enterprise_search import AppSearch, EnterpriseSearch, WorkplaceSearch
from tests.conftest import DummyNode


@pytest.mark.xfail
@pytest.mark.parametrize("request_timeout", [3, 5.0])
def test_request_timeout(request_timeout):
    client = EnterpriseSearch(node_class=DummyNode, meta_header=False)
    client.get_version(request_timeout=request_timeout)

    calls = client.transport.get_connection().calls
    assert calls == [
        (
            ("GET", "/api/ent/v1/internal/version", None),
            {
                "headers": {"user-agent": client._user_agent_header},
                "ignore_status": (),
                "request_timeout": request_timeout,
            },
        )
    ]


@pytest.mark.parametrize("client_cls", [EnterpriseSearch, AppSearch, WorkplaceSearch])
def test_client_class_init_parameters(client_cls):
    # Ensures that all client signatures are identical.
    sig = inspect.signature(client_cls)
    assert set(sig.parameters) == {
        "_transport",
        "basic_auth",
        "bearer_auth",
        "ca_certs",
        "client_cert",
        "client_key",
        "connections_per_node",
        "dead_node_backoff_factor",
        "headers",
        "hosts",
        "http_auth",
        "http_compress",
        "max_dead_node_backoff",
        "max_retries",
        "meta_header",
        "node_class",
        "request_timeout",
        "retry_on_status",
        "retry_on_timeout",
        "ssl_assert_fingerprint",
        "ssl_assert_hostname",
        "ssl_context",
        "ssl_show_warn",
        "ssl_version",
        "transport_class",
        "verify_certs",
    }
