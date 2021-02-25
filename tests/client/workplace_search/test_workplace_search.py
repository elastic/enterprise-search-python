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

import datetime

import pytest
from dateutil import tz

from elastic_enterprise_search import NotFoundError, UnauthorizedError, WorkplaceSearch

access_token = "b6e5d30d7e5248533b5a8f5362e16853e2fc32826bc940aa32bf3ff1f1748f9b"
content_source_id = "5f7e1407678c1d8435a949a8"

client_id = "1f87f8f6df473c06af79f88d1747afcb92e530295fad0fde340487673bec6ca6"
client_secret = "d26a2c9aaa5870e8d6bdf8169aaf21ce2d66ec2e0180ffc34a0390d254135311"
redirect_uri = "http://localhost:8000"
code = "7186fec34911a182606d2ab7fc36ea0ed4b8c32fef9929235cd80294422204ca"
refresh_token = "8be8a32c22f98a28d59cdd9d2c2028c97fa6367b77a1a41cc27f2264038ee8f3"


@pytest.fixture()
def workplace_search():
    yield WorkplaceSearch("http://localhost:3002", http_auth=access_token)


@pytest.mark.vcr()
def test_index_documents(workplace_search):
    dt = datetime.datetime(year=2019, month=6, day=1, hour=12, tzinfo=tz.UTC)
    resp = workplace_search.index_documents(
        content_source_id=content_source_id,
        documents=[
            {
                "id": 1234,
                "title": "The Meaning of Time",
                "body": "Not much. It is a made up thing.",
                "url": "https://example.com/meaning/of/time",
                "created_at": dt,
            },
            {
                "id": 1235,
                "title": "The Meaning of Sleep",
                "body": "Rest, recharge, and connect to the Ether.",
                "url": "https://example.com/meaning/of/sleep",
                "created_at": dt,
            },
        ],
    )
    assert resp.status == 200
    assert resp == {
        "results": [{"id": "1234", "errors": []}, {"id": "1235", "errors": []}]
    }


@pytest.mark.vcr()
def test_index_documents_content_source_not_found(workplace_search):
    with pytest.raises(NotFoundError) as e:
        workplace_search.index_documents(
            content_source_id=content_source_id + "a",
            documents=[
                {
                    "id": 1234,
                    "title": "The Meaning of Time",
                },
            ],
        )
    assert e.value.status == 404
    assert e.value.message == ""


@pytest.mark.vcr()
def test_oauth_exchange_for_access_token_code(workplace_search):
    resp = workplace_search.oauth_exchange_for_access_token(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        code="c6424958616f102ce4e8b9e776ac8547aa06c1a603a27970547648080c43abb9",
    )

    assert resp.status == 200
    assert resp == {
        "access_token": "00a456134c1964a0a9e82dff3ff93d8a20e9071a51f75b2bce18dde12908eb5d",
        "expires_in": 7200,
        "refresh_token": "57297c5f3a7fdf9dd63d03910c49c231d869e55e2e5934835c1ffa89c3c3b704",
        "scope": "search",
        "token_type": "Bearer",
    }


@pytest.mark.vcr()
def test_oauth_exchange_for_access_token_refresh_token(workplace_search):
    resp = workplace_search.oauth_exchange_for_access_token(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        refresh_token="57297c5f3a7fdf9dd63d03910c49c231d869e55e2e5934835c1ffa89c3c3b704",
    )

    assert resp.status == 200
    assert resp == {
        "access_token": "494c72a1acaab2ac1dcf06882d874f5e54ce50c82d6b7183374597c2aceaddd6",
        "expires_in": 7200,
        "refresh_token": "43fb836d0600ce7a6e18087d4a674277493ec7be03b88756fe531b266db997f4",
        "scope": "search",
        "token_type": "Bearer",
    }


@pytest.mark.vcr()
def test_oauth_exchange_for_access_token_invalid_grant(workplace_search):
    # The 'code' parameter has already been used for this example
    with pytest.raises(UnauthorizedError) as e:
        workplace_search.oauth_exchange_for_access_token(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            code="7186fec34911a182606d2ab7fc36ea0ed4b8c32fef9929235cd80294422204ca",
        )

    assert e.value.status == 401
    assert e.value.message == {
        "error": "invalid_grant",
        "error_description": "The provided authorization grant is invalid, expired, "
        "revoked, does not match the redirection URI used in the "
        "authorization request, or was issued to another client.",
    }
