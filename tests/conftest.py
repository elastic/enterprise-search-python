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

import os
from typing import Tuple

import pytest
import urllib3
from elastic_transport import ApiResponseMeta, BaseNode, HttpHeaders

from elastic_enterprise_search import AppSearch, EnterpriseSearch, WorkplaceSearch


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["user-agent", "x-elastic-client-meta"]}


@pytest.fixture(params=[EnterpriseSearch, AppSearch, WorkplaceSearch])
def client_class(request):
    return request.param


@pytest.fixture(scope="session")
def ent_search_url():
    url = "http://localhost:3002"
    urls_to_try = [
        "http://enterprise-search:3002",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ]
    if "ENTERPRISE_SEARCH_URL" in os.environ:
        urls_to_try.insert(0, os.environ["ENTERPRISE_SEARCH_URL"])
    for try_url in urls_to_try:
        try:
            http = urllib3.PoolManager()
            http.request("GET", try_url)
            url = try_url
            break
        except Exception:
            continue
    else:
        pytest.skip("No Enterprise Search instance running on 'localhost:3002'")
    return url


@pytest.fixture(scope="session")
def ent_search_basic_auth() -> Tuple[str, str]:
    try:
        yield ("elastic", os.environ["ENTERPRISE_SEARCH_PASSWORD"])
    except KeyError:
        pytest.skip("Skipped test because 'ENTERPRISE_SEARCH_PASSWORD' isn't set")


@pytest.fixture(scope="session")
def app_search_bearer_auth() -> str:
    try:
        yield os.environ["APP_SEARCH_PRIVATE_KEY"]
    except KeyError:
        pytest.skip("Skipped test because 'APP_SEARCH_PRIVATE_KEY' isn't set")


class DummyNode(BaseNode):
    def __init__(self, node_config, **kwargs):
        self.exception = kwargs.pop("exception", None)
        self.resp_status, self.resp_data = kwargs.pop("status", 200), kwargs.pop(
            "data", "{}"
        )
        self.resp_headers = kwargs.pop("headers", {})
        self.calls = []
        super().__init__(node_config)

    def perform_request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.exception:
            raise self.exception
        meta = ApiResponseMeta(
            status=self.resp_status,
            http_version="1.1",
            headers=HttpHeaders(self.resp_headers),
            duration=0.0,
            node=self.config,
        )
        return meta, self.resp_data
