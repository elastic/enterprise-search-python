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
from elastic_transport import Connection
from elastic_enterprise_search import (
    EnterpriseSearch,
    AppSearch,
    WorkplaceSearch,
)


@pytest.fixture(params=[EnterpriseSearch, AppSearch, WorkplaceSearch])
def client_class(request):
    return request.param


class DummyConnection(Connection):
    def __init__(self, **kwargs):
        self.exception = kwargs.pop("exception", None)
        self.status, self.data = kwargs.pop("status", 200), kwargs.pop("data", "{}")
        self.headers = kwargs.pop("headers", {})
        self.calls = []
        super(DummyConnection, self).__init__(**kwargs)

    def perform_request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.exception:
            raise self.exception
        return self.status, self.headers, self.data
