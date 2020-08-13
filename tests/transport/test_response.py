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
from elastic_enterprise_search.transport.response import Request, Response

req = Request(method="GET", path="/", headers={"header": "1"}, params={"param": 2})
resp_dict = Response(request=req, status_code=200, content={"key": "val"})
resp_list = Response(request=req, status_code=404, content=["a", 2, 3, {"k": "v"}])
resp_bool = Response(request=req, status_code=200, content=False)
all_resps = pytest.mark.parametrize("resp", [resp_bool, resp_dict, resp_list])


@all_resps
def test_response_equals(resp):
    assert resp == resp
    assert resp.content == resp
    assert resp == resp.content
    assert resp != object()

    resp_content_alt = type(resp.content)()
    if resp_content_alt is False:
        resp_content_alt = True
    assert resp != resp_content_alt


def test_response_not_equals():
    assert resp_dict != resp_list


def test_response_attributes():
    assert resp_bool.status_code == 200
    assert resp_bool.content is False
    assert resp_bool.request == req


def test_response_len():
    assert len(resp_dict) == 1
    assert len(resp_list) == 4

    with pytest.raises(TypeError):
        len(resp_bool)


def test_response_truthiness():
    assert bool(resp_dict) is True
    assert bool(resp_list) is True
    assert bool(resp_bool) is False


def test_response_contains():
    assert "key" in resp_dict
    assert 4 not in resp_list

    with pytest.raises(TypeError):
        "k" in resp_bool


def test_response_getitem():
    assert resp_dict["key"] == "val"
    assert resp_list[2] == 3

    with pytest.raises(TypeError):
        resp_bool[0]


def test_response_iter():
    for _ in resp_dict:
        pass
    for _ in resp_list:
        pass
    with pytest.raises(TypeError):
        for _ in resp_bool:
            pass


def test_response_getattr():
    resp_list.index(2)
    resp_dict.keys()
    resp_bool.bit_length()


@all_resps
def test_response_repr_str(resp):
    assert str(resp) == str(resp.content)
    assert repr(resp) == repr(resp.content)
