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

import random
import string

import pytest

from ..utils import pop_nested_json


@pytest.fixture(scope="function")
def engine_name(app_search):
    """Creates an engine with a randomized name which is removed after the test is completed."""
    engine_name = "test-engine-" + "".join(
        random.choice(string.ascii_lowercase) for _ in range(16)
    )
    app_search.options(ignore_status=404).delete_engine(engine_name=engine_name)
    app_search.create_engine(engine_name=engine_name)
    yield engine_name
    app_search.options(ignore_status=404).delete_engine(engine_name=engine_name)


def test_get_empty_engine(app_search, engine_name):
    resp = app_search.get_engine(engine_name=engine_name)
    assert resp == {
        "name": engine_name,
        "type": "default",
        "language": None,
        "document_count": 0,
        "index_create_settings_override": {},
    }


def test_crawler(app_search, engine_name):
    # Get empty crawler overview
    resp = app_search.get_crawler_overview(engine_name=engine_name)
    assert resp == {"domains": [], "events": [], "most_recent_crawl_request": None}

    # Create crawler domain
    resp = app_search.create_crawler_domain(
        engine_name=engine_name, body={"name": "https://www.elastic.co"}
    )
    resp = dict(resp)

    crawler_domain_id = resp.pop("id")
    entry_point_id = resp["entry_points"][0].pop("id")

    pop_nested_json(resp, "created_at")
    pop_nested_json(resp, "default_crawl_rule.created_at")
    pop_nested_json(resp, "entry_points.*.created_at")
    pop_nested_json(resp, "last_visited_at")

    assert resp == {
        "name": "https://www.elastic.co",
        "document_count": 0,
        "deduplication_enabled": True,
        "deduplication_fields": [
            "title",
            "body_content",
            "meta_keywords",
            "meta_description",
            "links",
            "headings",
        ],
        "available_deduplication_fields": [
            "title",
            "body_content",
            "meta_keywords",
            "meta_description",
            "links",
            "headings",
        ],
        "auth": None,
        "entry_points": [{"value": "/"}],
        "crawl_rules": [],
        "default_crawl_rule": {
            "id": "-",
            "order": 0,
            "policy": "allow",
            "rule": "regex",
            "pattern": ".*",
        },
        "sitemaps": [],
    }

    # Get crawler overview
    resp = app_search.get_crawler_overview(engine_name=engine_name)

    resp = dict(resp)
    pop_nested_json(resp, "domains.*.created_at")
    pop_nested_json(resp, "domains.*.default_crawl_rule.created_at")
    pop_nested_json(resp, "domains.*.entry_points.*.created_at")
    pop_nested_json(resp, "domains.*.last_visited_at")

    assert resp == {
        "domains": [
            {
                "auth": None,
                "available_deduplication_fields": [
                    "title",
                    "body_content",
                    "meta_keywords",
                    "meta_description",
                    "links",
                    "headings",
                ],
                "crawl_rules": [],
                "deduplication_enabled": True,
                "deduplication_fields": [
                    "title",
                    "body_content",
                    "meta_keywords",
                    "meta_description",
                    "links",
                    "headings",
                ],
                "default_crawl_rule": {
                    "id": "-",
                    "order": 0,
                    "pattern": ".*",
                    "policy": "allow",
                    "rule": "regex",
                },
                "document_count": 0,
                "entry_points": [
                    {
                        "id": entry_point_id,
                        "value": "/",
                    }
                ],
                "id": crawler_domain_id,
                "name": "https://www.elastic.co",
                "sitemaps": [],
            }
        ],
        "events": [],
        "most_recent_crawl_request": None,
    }

    # Create crawler rules
    resp = app_search.create_crawler_crawl_rule(
        engine_name=engine_name,
        domain_id=crawler_domain_id,
        body={"policy": "allow", "rule": "regex", "pattern": "^/$", "order": 0},
    )
    resp = dict(resp)
    crawl_rule_id = resp.pop("id")
    pop_nested_json(resp, "created_at")
    assert resp == {"policy": "allow", "rule": "regex", "pattern": "^/$", "order": 0}

    resp = app_search.create_crawler_crawl_rule(
        engine_name=engine_name,
        domain_id=crawler_domain_id,
        body={"policy": "deny", "rule": "regex", "pattern": ".*", "order": 1},
    )
    crawl_rule_id2 = resp["id"]

    # Create a sitemap
    resp = app_search.create_crawler_sitemap(
        engine_name=engine_name,
        domain_id=crawler_domain_id,
        body={"url": "https://elastic.co/sitemap.xml"},
    )
    resp = dict(resp)
    resp.pop("created_at")
    crawler_sitemap_id = resp.pop("id")
    assert resp == {"url": "https://elastic.co/sitemap.xml"}

    # Get domain
    resp = app_search.get_crawler_domain(
        engine_name=engine_name, domain_id=crawler_domain_id
    )
    resp = dict(resp)
    pop_nested_json(resp, "created_at")
    pop_nested_json(resp, "default_crawl_rule.created_at")
    pop_nested_json(resp, "entry_points.*.created_at")
    pop_nested_json(resp, "crawl_rules.*.created_at")
    pop_nested_json(resp, "sitemaps.*.created_at")
    pop_nested_json(resp, "last_visited_at")

    assert resp == {
        "id": crawler_domain_id,
        "name": "https://www.elastic.co",
        "document_count": 0,
        "deduplication_enabled": True,
        "deduplication_fields": [
            "title",
            "body_content",
            "meta_keywords",
            "meta_description",
            "links",
            "headings",
        ],
        "available_deduplication_fields": [
            "title",
            "body_content",
            "meta_keywords",
            "meta_description",
            "links",
            "headings",
        ],
        "entry_points": [
            {
                "id": entry_point_id,
                "value": "/",
            }
        ],
        "crawl_rules": [
            {
                "id": crawl_rule_id,
                "policy": "allow",
                "rule": "regex",
                "pattern": "^/$",
                "order": 0,
            },
            {
                "id": crawl_rule_id2,
                "policy": "deny",
                "rule": "regex",
                "pattern": ".*",
                "order": 1,
            },
        ],
        "default_crawl_rule": {
            "id": "-",
            "order": 0,
            "policy": "allow",
            "rule": "regex",
            "pattern": ".*",
        },
        "sitemaps": [
            {"id": crawler_sitemap_id, "url": "https://elastic.co/sitemap.xml"}
        ],
        "auth": None,
    }

    # Start a crawl
    resp = app_search.create_crawler_crawl_request(engine_name=engine_name)
    resp = dict(resp)
    crawl_request_id = resp.pop("id")
    resp.pop("created_at")
    assert resp == {
        "begun_at": None,
        "completed_at": None,
        "status": "pending",
        "type": "full",
    }

    # Cancel the crawl
    resp = app_search.delete_crawler_active_crawl_request(
        engine_name=engine_name,
    )
    resp = dict(resp)
    resp.pop("created_at")
    assert resp == {
        "begun_at": None,
        "completed_at": None,
        "id": crawl_request_id,
        "status": "canceling",
        "type": "full",
    }
