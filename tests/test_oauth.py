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

from elastic_enterprise_search import WorkplaceSearch

CLIENT_ID = "1f87f8f6df473c06af79f88d1747afcb92e530295fad0fde340487673bec6ca6"
CLIENT_SECRET = "d26a2c9aaa5870e8d6bdf8169aaf21ce2d66ec2e0180ffc34a0390d254135311"
REDIRECT_URI = "http://localhost:8000"
CODE = "7186fec34911a182606d2ab7fc36ea0ed4b8c32fef9929235cd80294422204ca"
REFRESH_TOKEN = "8be8a32c22f98a28d59cdd9d2c2028c97fa6367b77a1a41cc27f2264038ee8f3"


@pytest.mark.parametrize(
    ["response_type", "expected"],
    [
        (
            "token",
            (
                "http://localhost:3002/ws/oauth/authorize?response_type=token&"
                "client_id=1f87f8f6df473c06af79f88d1747afcb92e530295fad0fde340487673bec6ca6"
                "&redirect_uri=http%3A%2F%2Flocalhost%3A8000"
            ),
        ),
        (
            "code",
            (
                "http://localhost:3002/ws/oauth/authorize?response_type=code&"
                "client_id=1f87f8f6df473c06af79f88d1747afcb92e530295fad0fde340487673bec6ca6&"
                "redirect_uri=http%3A%2F%2Flocalhost%3A8000"
            ),
        ),
    ],
)
def test_oauth_authorize_url(response_type, expected):
    client = WorkplaceSearch("http://localhost:3002")

    assert expected == client.oauth_authorize_url(
        response_type=response_type, client_id=CLIENT_ID, redirect_uri=REDIRECT_URI
    )


def test_oauth_authorize_url_bad_input():
    client = WorkplaceSearch("http://localhost:3002")

    with pytest.raises(ValueError) as e:
        client.oauth_authorize_url(
            response_type="ye", client_id=CLIENT_ID, redirect_uri=REDIRECT_URI
        )
    assert (
        str(e.value)
        == "'response_type' must be either 'code' for confidential flowor 'token' for implicit flow"
    )

    with pytest.raises(TypeError) as e:
        client.oauth_authorize_url(
            response_type="token", client_id=1, redirect_uri=REDIRECT_URI
        )
    assert str(e.value) == "All parameters must be of type 'str'"


def test_oauth_exchange_for_token_bad_input():
    client = WorkplaceSearch("http://localhost:3002")

    with pytest.raises(ValueError) as e:
        client.oauth_exchange_for_access_token(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI
        )
    assert str(e.value) == "Either the 'code' or 'refresh_token' parameter must be used"

    with pytest.raises(ValueError) as e:
        client.oauth_exchange_for_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            code="hello",
            refresh_token="world",
        )
    assert (
        str(e.value) == "'code' and 'refresh_token' parameters are mutually exclusive"
    )

    with pytest.raises(TypeError) as e:
        client.oauth_exchange_for_access_token(
            client_id=1,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            code=CODE,
        )
    assert str(e.value) == "All parameters must be of type 'str'"
