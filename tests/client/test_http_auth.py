# -*- coding: utf-8 -*-
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

from elastic_enterprise_search._utils import DEFAULT
from tests.conftest import DummyConnection


def test_http_auth_none(client_class):
    client = client_class(connection_class=DummyConnection, meta_header=False)
    assert client.http_auth is None
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert calls == [
        (
            ("GET", "/", None),
            {
                "headers": {"user-agent": client._user_agent_header},
                "ignore_status": (),
                "request_timeout": DEFAULT,
            },
        )
    ]

    client = client_class(
        http_auth=None, connection_class=DummyConnection, meta_header=False
    )
    assert client.http_auth is None
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert calls == [
        (
            ("GET", "/", None),
            {
                "headers": {"user-agent": client._user_agent_header},
                "ignore_status": (),
                "request_timeout": DEFAULT,
            },
        )
    ]


@pytest.mark.parametrize(
    "http_auth", ["this-is-a-token", ("user", "password"), (u"üser", u"pӓssword")]
)
def test_http_auth_set_and_get(client_class, http_auth):
    client = client_class(http_auth=http_auth, connection_class=DummyConnection)
    assert client.http_auth == http_auth
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert len(calls) == 1
    assert calls[0][1]["headers"]["authorization"] == client._authorization_header


def test_http_auth_per_request_override(client_class):
    client = client_class(http_auth="bad-token", connection_class=DummyConnection)
    assert client.http_auth == "bad-token"
    client.perform_request("GET", "/", http_auth=("user", "pass"))

    calls = client.transport.get_connection().calls
    assert len(calls) == 1
    assert calls[0][1]["headers"]["authorization"] == "Basic dXNlcjpwYXNz"

    # Client.http_auth doesn't get overwritten
    assert client.http_auth == "bad-token"


def test_http_auth_object(client_class):
    with pytest.raises(TypeError) as err:
        client_class(http_auth=object())
    assert str(err.value) == (
        "'http_auth' must either be a tuple of (username, password) "
        "for 'Basic' authentication or a single string for 'Bearer'/token authentication"
    )

    client = client_class()
    with pytest.raises(TypeError) as err:
        client.http_auth = object()
    assert str(err.value) == (
        "'http_auth' must either be a tuple of (username, password) "
        "for 'Basic' authentication or a single string for 'Bearer'/token authentication"
    )


def test_http_auth_disable_with_none(client_class):
    client = client_class(http_auth="api-token", connection_class=DummyConnection)
    assert client.http_auth == "api-token"
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert len(calls) == 1
    assert calls[0][1]["headers"]["authorization"] == client._authorization_header

    client.perform_request("GET", "/", http_auth=None)

    calls = client.transport.get_connection().calls
    assert len(calls) == 2
    assert "authorization" not in calls[-1][1]["headers"]

    client.http_auth = None
    assert client.http_auth is None
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert len(calls) == 3
    assert "authorization" not in calls[-1][1]["headers"]
