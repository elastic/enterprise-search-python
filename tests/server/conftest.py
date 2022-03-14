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


@pytest.fixture(scope="session")
def ent_search(ent_search_url):
    with EnterpriseSearch(ent_search_url, basic_auth=("elastic", "changeme")) as client:
        yield client


@pytest.fixture(scope="session")
def app_search(ent_search):
    client = ent_search.app_search
    client.basic_auth = ("elastic", "7XdP3UGdKcFq4D6JfZC4VPzB")
    yield client
