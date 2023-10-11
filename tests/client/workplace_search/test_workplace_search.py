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
import random
import string

import pytest
from dateutil import tz

from elastic_enterprise_search import NotFoundError, UnauthorizedError, WorkplaceSearch

access_token = "b6e5d30d7e5248533b5a8f5362e16853e2fc32826bc940aa32bf3ff1f1748f9b"
content_source_id = "5f7e1407678c1d8435a949a8"

CLIENT_ID = "1f87f8f6df473c06af79f88d1747afcb92e530295fad0fde340487673bec6ca6"
CLIENT_SECRET = "d26a2c9aaa5870e8d6bdf8169aaf21ce2d66ec2e0180ffc34a0390d254135311"
OAUTH_REDIRECT_URI = "http://localhost:8000"
OAUTH_CODE = "7186fec34911a182606d2ab7fc36ea0ed4b8c32fef9929235cd80294422204ca"
OAUTH_REFRESH_TOKEN = "8be8a32c22f98a28d59cdd9d2c2028c97fa6367b77a1a41cc27f2264038ee8f3"


@pytest.fixture()
def vcr_workplace_search():
    yield WorkplaceSearch("http://localhost:3002", bearer_auth=access_token)


@pytest.fixture()
def workplace_search(ent_search_url, ent_search_basic_auth):
    with WorkplaceSearch(ent_search_url, basic_auth=ent_search_basic_auth) as client:
        yield client


@pytest.fixture(scope="function")
def content_source(workplace_search):
    resp = workplace_search.create_content_source(
        name=f"Custom Content Source {''.join(random.choice(string.ascii_letters) for _ in range(16))}"
    )
    content_source_id = resp["id"]
    yield content_source_id
    workplace_search.delete_content_source(content_source_id=content_source_id)


def test_content_sources(workplace_search, content_source):
    resp = workplace_search.get_content_source(content_source_id=content_source)
    assert resp.meta.status == 200

    content_source_json = resp.body.copy()
    for field in ("name", "created_at", "last_updated_at", "groups"):
        resp.body.pop(field)

    assert resp == {
        "id": content_source,
        "service_type": "custom",
        "is_remote": False,
        "details": [],
        "context": "organization",
        "is_searchable": True,
        "facets": {"overrides": []},
        "automatic_query_refinement": {"overrides": []},
        "schema": {},
        "display": {
            "title_field": "",
            "subtitle_field": "",
            "description_field": "",
            "url_field": "",
            "type_field": "",
            "media_type_field": "",
            "created_by_field": "",
            "updated_by_field": "",
            "detail_fields": [],
            "color": "#000000",
        },
        "document_count": 0,
        "last_indexed_at": None,
    }

    resp = workplace_search.list_content_sources()
    assert resp.meta.status == 200
    assert resp == {
        "meta": {
            "page": {"current": 1, "total_pages": 1, "total_results": 1, "size": 25}
        },
        "results": [content_source_json],
    }


def test_documents(workplace_search, content_source):
    dt = datetime.datetime(year=2019, month=6, day=1, hour=12, tzinfo=tz.UTC)
    resp = workplace_search.index_documents(
        content_source_id=content_source,
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
    assert resp.meta.status == 200
    assert resp == {
        "results": [{"id": "1234", "errors": []}, {"id": "1235", "errors": []}]
    }

    resp = workplace_search.get_document(
        content_source_id=content_source, document_id="1234"
    )
    assert resp.meta.status == 200

    for field in ("created_at", "updated_at", "last_updated"):
        resp.body.pop(field)
    assert resp == {
        "title": "The Meaning of Time",
        "body": "Not much. It is a made up thing.",
        "url": "https://example.com/meaning/of/time",
        "source": "custom",
        "content_source_id": content_source,
        "id": "1234",
    }

    resp = workplace_search.delete_documents_by_query(content_source_id=content_source)
    assert resp.meta.status == 200
    assert resp.body == {"deleted": 2, "failures": [], "total": 2}


@pytest.mark.vcr()
def test_index_documents_content_source_not_found(vcr_workplace_search):
    with pytest.raises(NotFoundError) as e:
        vcr_workplace_search.index_documents(
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
def test_oauth_exchange_for_access_token_code(vcr_workplace_search):
    resp = vcr_workplace_search.oauth_exchange_for_access_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=OAUTH_REDIRECT_URI,
        code="c6424958616f102ce4e8b9e776ac8547aa06c1a603a27970547648080c43abb9",
    )

    assert resp.meta.status == 200
    assert resp == {
        "access_token": "00a456134c1964a0a9e82dff3ff93d8a20e9071a51f75b2bce18dde12908eb5d",
        "expires_in": 7200,
        "refresh_token": "57297c5f3a7fdf9dd63d03910c49c231d869e55e2e5934835c1ffa89c3c3b704",
        "scope": "search",
        "token_type": "Bearer",
    }


@pytest.mark.vcr()
def test_oauth_exchange_for_access_token_refresh_token(vcr_workplace_search):
    resp = vcr_workplace_search.oauth_exchange_for_access_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=OAUTH_REDIRECT_URI,
        refresh_token="57297c5f3a7fdf9dd63d03910c49c231d869e55e2e5934835c1ffa89c3c3b704",
    )

    assert resp.meta.status == 200
    assert resp == {
        "access_token": "494c72a1acaab2ac1dcf06882d874f5e54ce50c82d6b7183374597c2aceaddd6",
        "expires_in": 7200,
        "refresh_token": "43fb836d0600ce7a6e18087d4a674277493ec7be03b88756fe531b266db997f4",
        "scope": "search",
        "token_type": "Bearer",
    }


@pytest.mark.vcr()
def test_oauth_exchange_for_access_token_invalid_grant(vcr_workplace_search):
    # The 'code' parameter has already been used for this example
    with pytest.raises(UnauthorizedError) as e:
        vcr_workplace_search.oauth_exchange_for_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=OAUTH_REDIRECT_URI,
            code="7186fec34911a182606d2ab7fc36ea0ed4b8c32fef9929235cd80294422204ca",
        )

    assert e.value.meta.status == 401
    assert e.value.body == {
        "error": "invalid_grant",
        "error_description": "The provided authorization grant is invalid, expired, "
        "revoked, does not match the redirection URI used in the "
        "authorization request, or was issued to another client.",
    }
