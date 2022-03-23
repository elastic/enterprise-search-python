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


def test_get_version(ent_search):
    assert set(ent_search.get_version()) == {"number", "build_hash", "build_date"}


@pytest.mark.parametrize("include", [["app", "queues"], ("app", "queues")])
def test_get_stats_include(ent_search: EnterpriseSearch, include):
    with pytest.raises(ValueError) as e:
        ent_search.get_stats(include="queues")
    assert str(e.value) == "'include' must be of type list or tuple"

    resp = ent_search.get_stats()
    assert resp.meta.status == 200
    assert set(resp.body.keys()) == {
        "app",
        "cluster_uuid",
        "connectors",
        "crawler",
        "http",
        "product_usage",
        "queues",
    }

    resp = ent_search.get_stats(include=include)
    assert resp.meta.status == 200
    assert set(resp.body.keys()) == {"app", "queues"}
