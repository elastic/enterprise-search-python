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

from elastic_enterprise_search import Transport, ConnectionError
from elastic_enterprise_search.transport.connection_pool import DummyConnectionPool
from tests.conftest import DummyConnection

import pytest


def test_single_connection_uses_dummy_connection_pool():
    t = Transport([{}])
    assert isinstance(t.connection_pool, DummyConnectionPool)
    t = Transport([{"host": "localhost"}])
    assert isinstance(t.connection_pool, DummyConnectionPool)


def test_request_timeout_extracted_from_params_and_passed():
    t = Transport([{}], connection_class=DummyConnection)

    t.perform_request("GET", "/", params={"request_timeout": 42})
    assert 1 == len(t.get_connection().calls)
    assert ("GET", "/", {}, None) == t.get_connection().calls[0][0]
    assert {"timeout": 42, "ignore": (), "headers": None} == t.get_connection().calls[
        0
    ][1]


def test_opaque_id():
    t = Transport([{}], opaque_id="app-1", connection_class=DummyConnection)

    t.perform_request("GET", "/")
    assert 1 == len(t.get_connection().calls)
    assert ("GET", "/", None, None) == t.get_connection().calls[0][0]
    assert {"timeout": None, "ignore": (), "headers": None} == t.get_connection().calls[
        0
    ][1]

    # Now try with an 'x-opaque-id' set on perform_request().
    t.perform_request("GET", "/", headers={"x-opaque-id": "request-1"})
    assert 2 == len(t.get_connection().calls)
    assert ("GET", "/", None, None) == t.get_connection().calls[1][0]
    assert {
        "timeout": None,
        "ignore": (),
        "headers": {"x-opaque-id": "request-1"},
    } == t.get_connection().calls[1][1]


def test_request_with_custom_user_agent_header():
    t = Transport([{}], connection_class=DummyConnection)

    t.perform_request("GET", "/", headers={"user-agent": "my-custom-value/1.2.3"})
    assert 1 == len(t.get_connection().calls)
    assert {
        "timeout": None,
        "ignore": (),
        "headers": {"user-agent": "my-custom-value/1.2.3"},
    } == t.get_connection().calls[0][1]


def test_body_gets_encoded_into_bytes():
    t = Transport([{}], connection_class=DummyConnection)

    t.perform_request("GET", "/", body="你好")
    assert 1 == len(t.get_connection().calls)
    assert ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd") == t.get_connection().calls[
        0
    ][0]


def test_body_bytes_get_passed_untouched():
    t = Transport([{}], connection_class=DummyConnection)

    body = b"\xe4\xbd\xa0\xe5\xa5\xbd"
    t.perform_request("GET", "/", body=body)
    assert 1 == len(t.get_connection().calls)
    assert ("GET", "/", None, body) == t.get_connection().calls[0][0]


def test_body_surrogates_replaced_encoded_into_bytes():
    t = Transport([{}], connection_class=DummyConnection)

    t.perform_request("GET", "/", body="你好\uda6a")
    assert 1 == len(t.get_connection().calls)
    assert (
        "GET",
        "/",
        None,
        b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa",
    ) == t.get_connection().calls[0][0]


def test_kwargs_passed_on_to_connections():
    t = Transport([{"host": "google.com"}], port=123)
    assert 1 == len(t.connection_pool.connections)
    assert "http://google.com:123" == t.connection_pool.connections[0].host


def test_kwargs_passed_on_to_connection_pool():
    dt = object()
    t = Transport([{}, {}], dead_timeout=dt)
    assert dt is t.connection_pool.dead_timeout


def test_custom_connection_class():
    class MyConnection(object):
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    t = Transport([{}], connection_class=MyConnection)
    assert 1 == len(t.connection_pool.connections)
    assert isinstance(t.connection_pool.connections[0], MyConnection)


def test_add_connection():
    t = Transport([{}], randomize_hosts=False)
    t.add_connection({"host": "google.com", "port": 1234})

    assert 2 == len(t.connection_pool.connections)
    assert "http://google.com:1234" == t.connection_pool.connections[1].host


def test_request_will_fail_after_X_retries():
    t = Transport(
        [{"exception": ConnectionError("abandon ship")}],
        connection_class=DummyConnection,
    )

    with pytest.raises(ConnectionError):
        t.perform_request("GET", "/")
    assert 4 == len(t.get_connection().calls)


def test_failed_connection_will_be_marked_as_dead():
    t = Transport(
        [{"exception": ConnectionError("abandon ship")}] * 2,
        connection_class=DummyConnection,
    )

    with pytest.raises(ConnectionError):
        t.perform_request("GET", "/")
    assert 0 == len(t.connection_pool.connections)


def test_resurrected_connection_will_be_marked_as_live_on_success():
    for method in ("GET", "HEAD"):
        t = Transport([{}, {}], connection_class=DummyConnection)
        con1 = t.connection_pool.get_connection()
        con2 = t.connection_pool.get_connection()
        t.connection_pool.mark_dead(con1)
        t.connection_pool.mark_dead(con2)

        t.perform_request(method, "/")
        assert 1 == len(t.connection_pool.connections)
        assert 1 == len(t.connection_pool.dead_count)
