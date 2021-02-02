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

from elastic_enterprise_search import EnterpriseSearch


@pytest.fixture()
def enterprise_search():
    yield EnterpriseSearch("http://localhost:3002", http_auth=("elastic", "changeme"))


@pytest.mark.vcr()
def test_get_stats(enterprise_search):
    resp = enterprise_search.get_stats()
    assert resp.status == 200
    assert sorted(resp.keys()) == ["app", "connectors", "queues"]

    resp = enterprise_search.get_stats(include=["connectors", "queues"])
    assert resp.status == 200
    assert sorted(resp.keys()) == ["connectors", "queues"]


@pytest.mark.vcr()
def test_get_health(enterprise_search):
    resp = enterprise_search.get_health()
    assert resp.status == 200
    assert sorted(resp.keys()) == [
        "esqueues_me",
        "filebeat",
        "jvm",
        "name",
        "system",
        "version",
    ]
    assert resp["version"] == {
        "build_date": "2021-01-06T15:24:44Z",
        "build_hash": "3a6edf8029dd285b60f1a6d63c741f46df7f195f",
        "number": "7.12.0",
    }


@pytest.mark.vcr()
def test_get_version(enterprise_search):
    resp = enterprise_search.get_health()
    assert resp.status == 200
    assert sorted(resp.keys()) == [
        "esqueues_me",
        "filebeat",
        "jvm",
        "name",
        "system",
        "version",
    ]
    assert resp["version"] == {
        "build_date": "2021-01-06T15:24:44Z",
        "build_hash": "3a6edf8029dd285b60f1a6d63c741f46df7f195f",
        "number": "7.12.0",
    }


@pytest.mark.vcr()
def test_get_and_put_read_only(enterprise_search):
    http_auth = ("elastic", "changeme")
    resp = enterprise_search.put_read_only(body={"enabled": True}, http_auth=http_auth)
    assert resp.status == 200
    assert resp == {"enabled": True}

    resp = enterprise_search.get_read_only(http_auth=http_auth)
    assert resp.status == 200
    assert resp == {"enabled": True}

    resp = enterprise_search.put_read_only(body={"enabled": False}, http_auth=http_auth)
    assert resp.status == 200
    assert resp == {"enabled": False}
