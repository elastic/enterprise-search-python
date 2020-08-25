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
import urllib3
from elastic_enterprise_search import EnterpriseSearch


@pytest.fixture(scope="session")
def ent_search():
    host = "localhost"
    for try_host in ("enterprise-search", "localhost", "127.0.0.1"):
        try:
            http = urllib3.PoolManager()
            http.request("GET", "http://%s:3002" % try_host)
            host = try_host
            break
        except Exception:
            continue
    else:
        pytest.skip("No Enterprise Search instance running on 'localhost:3002'")

    # TODO: Add authentication to this client
    with EnterpriseSearch("http://%s:3002" % host) as client:
        yield client
