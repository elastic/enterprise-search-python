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

from elastic_enterprise_search import AsyncAppSearch, NotFoundError


@pytest.mark.asyncio
async def test_engines(app_search: AsyncAppSearch):
    await app_search.options(ignore_status=404).delete_engine(
        engine_name="example-engine"
    )

    resp = await app_search.create_engine(engine_name="example-engine")
    assert resp.meta.status == 200
    assert resp.body == {
        "document_count": 0,
        "index_create_settings_override": {},
        "language": None,
        "name": "example-engine",
        "type": "default",
    }

    resp = await app_search.list_engines()
    assert resp.meta.status == 200
    assert {
        "name": "example-engine",
        "type": "default",
        "language": None,
        "index_create_settings_override": {},
        "document_count": 0,
    } in resp.body["results"]

    resp = await app_search.delete_engine(engine_name="example-engine")
    assert resp.meta.status == 200
    assert resp.body == {"deleted": True}


@pytest.mark.asyncio
async def test_error(app_search: AsyncAppSearch):
    with pytest.raises(NotFoundError) as e:
        await app_search.get_engine(engine_name="does-not-exist")

    assert e.value.meta.status == 404
    assert e.value.message == "{'errors': ['Could not find engine.']}"
    assert e.value.body == {"errors": ["Could not find engine."]}
