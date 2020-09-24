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
from tests.conftest import DummyConnection
from elastic_enterprise_search import EnterpriseSearch


@pytest.mark.parametrize("request_timeout", [3, 5.0])
def test_request_timeout(request_timeout):
    client = EnterpriseSearch(connection_class=DummyConnection)
    client.get_version(request_timeout=request_timeout)

    calls = client.transport.get_connection().calls
    assert calls == [
        (
            ("GET", "/api/ent/v1/internal/version", None, None),
            {
                "headers": {"user-agent": client._user_agent_header},
                "ignore_status": (),
                "request_timeout": request_timeout,
            },
        )
    ]
