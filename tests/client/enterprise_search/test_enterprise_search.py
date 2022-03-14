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
    yield EnterpriseSearch(
        "https://my-deployment-c6095a.ent.us-central1.gcp.cloud.es.io:443",
        basic_auth=("elastic", "yqcGpRqU9Mk4FQmsvJKxL9Uo"),
    )


@pytest.mark.vcr()
def test_get_stats(enterprise_search):
    resp = enterprise_search.get_stats()
    assert resp.meta.status == 200
    assert sorted(resp.keys()) == [
        "app",
        "cluster_uuid",
        "connectors",
        "crawler",
        "http",
        "product_usage",
        "queues",
    ]

    resp = enterprise_search.get_stats(include=["connectors", "queues"])
    assert resp.meta.status == 200
    assert sorted(resp.keys()) == ["connectors", "queues"]


@pytest.mark.vcr()
def test_get_health(enterprise_search):
    resp = enterprise_search.get_health()
    assert resp.meta.status == 200
    assert sorted(resp.keys()) == [
        "cluster_uuid",
        "crawler",
        "esqueues_me",
        "filebeat",
        "jvm",
        "metricbeat",
        "name",
        "system",
        "version",
    ]
    assert resp["version"] == {
        "number": "8.1.0",
        "build_hash": "233d9108d258845ddd4a36915d45e22c19024981",
        "build_date": "2022-03-03T14:31:36+00:00",
    }


@pytest.mark.vcr()
def test_get_version(enterprise_search):
    resp = enterprise_search.get_version()
    assert resp.meta.status == 200
    assert resp == {
        "number": "8.1.0",
        "build_hash": "233d9108d258845ddd4a36915d45e22c19024981",
        "build_date": "2022-03-03T14:31:36+00:00",
    }


@pytest.mark.vcr()
def test_get_and_put_read_only(enterprise_search):
    resp = enterprise_search.put_read_only(body={"enabled": True})
    assert resp.meta.status == 200
    assert resp == {"enabled": True}

    resp = enterprise_search.get_read_only()
    assert resp.meta.status == 200
    assert resp == {"enabled": True}

    resp = enterprise_search.put_read_only(enabled=False)
    assert resp.meta.status == 200
    assert resp == {"enabled": False}
