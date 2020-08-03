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


def test_http_auth_none(client_class):
    client = client_class()
    assert "authorization" not in client.transport.headers
    assert client.http_auth is None

    client = client_class(http_auth=None)
    assert "authorization" not in client.transport.headers
    assert client.http_auth is None


@pytest.mark.parametrize(
    "http_auth", ["this-is-a-token", ("user", "password"), (u"üser", u"pӓssword")]
)
def test_http_auth_set_and_get(client_class, http_auth):
    client = client_class(http_auth=http_auth)

    assert "authorization" in client.transport.headers
    assert client.http_auth == http_auth


def test_bad_basic_auth(client_class):
    client = client_class(headers={"authorization": "Basic thisaintproper"})
    assert client.http_auth == "thisaintproper"


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
