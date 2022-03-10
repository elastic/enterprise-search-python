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

from elastic_enterprise_search import EnterpriseSearch


def test_httpbin():
    client = EnterpriseSearch("https://httpbin.org:443")
    resp = client.perform_request("GET", "/anything")
    assert resp.meta.status == 200
    assert re.match(
        r"^ent=8[.0-9]+p?,py=[.0-9]+p?,t=[.0-9]+p?,ur=[.0-9]+p?$",
        resp.body["headers"]["X-Elastic-Client-Meta"],
    )
    assert resp.body["headers"]["User-Agent"].startswith("enterprise-search-python/")
