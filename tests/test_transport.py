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
from platform import python_version
from elastic_enterprise_search import __version__, Transport


def test_user_agent_default():
    t = Transport()
    assert t.headers["user-agent"] == "enterprise-search-python/%s (Python %s)" % (
        __version__,
        python_version(),
    )

    t = Transport(headers={"User-Agent": "non-default/1.0"})
    assert t.headers["user-agent"] == "non-default/1.0"


def test_default_base_url():
    t = Transport()
    assert t._base_url == "http://localhost:3002"

    t = Transport(use_ssl=True)
    assert t._base_url == "https://localhost:3002"

    t = Transport(port=3003, use_ssl=True)
    assert t._base_url == "https://localhost:3003"


def test_host_as_url():
    t = Transport("http://hostname:1234")
    assert t._base_url == "http://hostname:1234"

    t = Transport("https://hostname")
    assert t._base_url == "https://hostname"


def test_host_ipv6():
    t = Transport("http://[::1]:3200")
    assert t._base_url == "http://[::1]:3200"

    t = Transport("http://[::1]:3002", port=3002)
    assert t._base_url == "http://[::1]:3002"

    t = Transport("http://[::1]", port=3002)
    assert t._base_url == "http://[::1]:3002"

    t = Transport("[::1]")
    assert t._base_url == "http://[::1]"

    t = Transport("::1", use_ssl=True, port=8080)
    assert t._base_url == "https://[::1]:8080"


def test_authority_errors():
    with pytest.raises(ValueError) as err:
        Transport("ssh://localhost")
    assert str(err.value) == "Invalid scheme in 'host' ('ssh')"

    with pytest.raises(ValueError) as err:
        Transport("http://localhost:8080", port=8000)
    assert (
        str(err.value)
        == "Conflicting ports specified in both 'host' (8080) and 'port' (8000) parameter"
    )

    with pytest.raises(ValueError) as err:
        Transport("https://localhost", use_ssl=False)
    assert (
        str(err.value)
        == "Conflicting schemes specified in both 'host' ('https') and 'use_ssl' (False)"
    )

    with pytest.raises(ValueError) as err:
        Transport("http://localhost", use_ssl=True)
    assert (
        str(err.value)
        == "Conflicting schemes specified in both 'host' ('http') and 'use_ssl' (True)"
    )


def test_default_headers():
    t = Transport()
    assert sorted(t.headers.keys()) == ["accept", "accept-encoding", "user-agent"]
    assert t.headers["accept"] == "application/json"
    assert t.headers["accept-encoding"] == "gzip"

    t = Transport(headers={"Accept": "ac", "Accept-Encoding": "ae", "Custom": "header"})
    assert sorted(t.headers.keys()) == [
        "accept",
        "accept-encoding",
        "custom",
        "user-agent",
    ]
    assert t.headers["accept"] == "ac"
    assert t.headers["accept-encoding"] == "ae"
    assert t.headers["custom"] == "header"
