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

import re

import pytest

from tests.conftest import DummyNode


def test_client_meta_header_http_meta(client_class):
    # Test with HTTP connection meta
    class DummyNodeWithMeta(DummyNode):
        _CLIENT_META_HTTP_CLIENT = ("dm", "1.2.3")

    client = client_class(node_class=DummyNodeWithMeta)
    assert client.http_auth is None
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert len(calls) == 1
    headers = calls[0][1]["headers"]
    assert re.match(
        r"^ent=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?,dm=[0-9.]+p?$",
        headers["x-elastic-client-meta"],
    )


def test_client_meta_header_no_http_meta(client_class):
    # Test without an HTTP connection meta
    client = client_class(node_class=DummyNode)
    assert client.http_auth is None
    client.perform_request("GET", "/")

    calls = client.transport.get_connection().calls
    assert len(calls) == 1
    headers = calls[0][1]["headers"]
    assert re.match(
        r"^ent=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?$", headers["x-elastic-client-meta"]
    )


def test_client_meta_header_extra_meta(client_class):
    class DummyNodeWithMeta(DummyNode):
        _CLIENT_META_HTTP_CLIENT = ("dm", "1.2.3")

    client = client_class(node_class=DummyNodeWithMeta)
    assert client.http_auth is None
    client.perform_request("GET", "/", params={"__elastic_client_meta": (("h", "pg"),)})

    calls = client.transport.get_connection().calls
    assert len(calls) == 1
    headers = calls[0][1]["headers"]
    assert re.match(
        r"^ent=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?,dm=[0-9.]+,h=pg?$",
        headers["x-elastic-client-meta"],
    )


def test_client_meta_header_type_error(client_class):
    with pytest.raises(TypeError) as e:
        client_class(meta_header=1)
    assert str(e.value) == "meta_header must be of type bool"
