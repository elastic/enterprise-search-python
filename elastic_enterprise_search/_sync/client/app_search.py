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

import typing as t

from elastic_transport import ObjectApiResponse

from ..._utils import SKIP_IN_PATH, _quote, _rewrite_parameters
from ._base import BaseClient


class AppSearch(BaseClient):
    @_rewrite_parameters(body_name="body", ignore_deprecated_options={"body", "params"})
    def search_es_search(
        self,
        *,
        engine_name: str,
        params: t.Optional[t.Mapping[str, t.Any]] = None,
        body: t.Optional[t.Mapping[str, t.Any]] = None,
        analytics_query: t.Optional[str] = None,
        analytics_tags: t.Optional[t.Union[str, t.Sequence[str]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Execute the provided Elasticsearch search query against an App Search Engine

        `<https://www.elastic.co/guide/en/app-search/current/elasticsearch-search-api-reference.html>`_

        :param engine_name: Name of the engine
        :param params: Query parameters for the Elasticsearch Search request.
        :param body: Body parameters for the Elasticsearch Search request.
        :param analytics_query: The search query associated with this request when recording search analytics.
        :param analytics_tags: The tags to apply to the query when recording search analytics.
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")

        if params is not None and any(not isinstance(x, str) for x in params.values()):
            raise TypeError("Values for 'params' parameter must be of type 'str'")

        __headers = {"accept": "application/json", "content-type": "application/json"}
        if analytics_query is not None:
            __headers["X-Enterprise-Search-Analytics"] = analytics_query
        if analytics_tags is not None:
            if isinstance(analytics_tags, str):
                analytics_tags = (analytics_tags,)
            __headers["X-Enterprise-Search-Analytics-Tags"] = ",".join(analytics_tags)

        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v0/engines/{_quote(engine_name)}/elasticsearch/_search",
            params=params,
            body=body,
            headers=__headers,
        )

    # AUTO-GENERATED-API-DEFINITIONS #

    @_rewrite_parameters()
    def get_adaptive_relevance_settings(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve adaptive relevance settings

        `<https://www.elastic.co/guide/en/app-search/current/adaptive-relevance-api-reference.html#adaptive-relevance-api-get-engine-adaptive-relevance-settings>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v0/engines/{_quote(engine_name)}/adaptive_relevance/settings",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_adaptive_relevance_settings(
        self,
        *,
        engine_name: str,
        curation: t.Mapping[str, t.Any],
    ) -> ObjectApiResponse[t.Any]:
        """
        Update adaptive relevance settings

        `<https://www.elastic.co/guide/en/app-search/current/adaptive-relevance-api-reference.html#adaptive-relevance-api-put-engine-adaptive-relevance-settings>`_

        :param engine_name: Name of the engine
        :param curation:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if curation is None:
            raise ValueError("Empty value passed for parameter 'curation'")
        __body: t.Dict[str, t.Any] = {}
        if curation is not None:
            __body["curation"] = curation
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v0/engines/{_quote(engine_name)}/adaptive_relevance/settings",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def list_adaptive_relevance_suggestions(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve adaptive relevance

        `<https://www.elastic.co/guide/en/app-search/current/adaptive-relevance-api-reference.html#adaptive-relevance-api-get-engine-adaptive-relevance-suggestions>`_

        :param engine_name: Name of the engine
        :param current_page:
        :param filters:
        :param page_size:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if filters is not None:
            __body["filters"] = filters
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v0/engines/{_quote(engine_name)}/adaptive_relevance/suggestions",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def put_adaptive_relevance_suggestions(
        self,
        *,
        engine_name: str,
        body: t.Union[
            t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
        ],
    ) -> ObjectApiResponse[t.Any]:
        """
        Update adaptive relevance

        `<https://www.elastic.co/guide/en/app-search/current/adaptive-relevance-api-reference.html#adaptive-relevance-api-put-engine-adaptive-relevance-suggestions>`_

        :param engine_name: Name of the engine
        :param body:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v0/engines/{_quote(engine_name)}/adaptive_relevance/suggestions",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def get_adaptive_relevance_suggestions(
        self,
        *,
        engine_name: str,
        search_suggestion_query: str,
        current_page: t.Optional[int] = None,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve adaptive relevance for a single query

        `<https://www.elastic.co/guide/en/app-search/current/adaptive-relevance-api-reference.html#adaptive-relevance-api-get-engine-adaptive-relevance-suggestions-query>`_

        :param engine_name: Name of the engine
        :param search_suggestion_query: Query to obtain suggestions
        :param current_page:
        :param filters:
        :param page_size:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if search_suggestion_query in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for parameter 'search_suggestion_query'"
            )
        __body: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if filters is not None:
            __body["filters"] = filters
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v0/engines/{_quote(engine_name)}/adaptive_relevance/suggestions/{_quote(search_suggestion_query)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def refresh_adaptive_relevance_update_process(
        self,
        *,
        engine_name: str,
        adaptive_relevance_suggestion_type: t.Union["t.Literal['curation']", str],
    ) -> ObjectApiResponse[t.Any]:
        """
        Update suggestions process refresh

        `<https://www.elastic.co/guide/en/app-search/current/adaptive-relevance-api-reference.html#adaptive-relevance-api-post-engine-adaptive-relevance-suggestions-update-process-refresh>`_

        :param engine_name: Name of the engine
        :param adaptive_relevance_suggestion_type: Adaptive relevance suggestion type
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if adaptive_relevance_suggestion_type in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for parameter 'adaptive_relevance_suggestion_type'"
            )
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v0/engines/{_quote(engine_name)}/adaptive_relevance/update_process/{_quote(adaptive_relevance_suggestion_type)}/refresh",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def get_top_clicks_analytics(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
        query: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns the number of clicks received by a document in descending order

        `<https://www.elastic.co/guide/en/app-search/current/clicks.html>`_

        :param engine_name: Name of the engine
        :param current_page:
        :param filters:
        :param page_size:
        :param query:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if filters is not None:
            __body["filters"] = filters
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        if query is not None:
            __body["query"] = query
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/analytics/clicks",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def get_count_analytics(
        self,
        *,
        engine_name: str,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        interval: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns the number of clicks and total number of queries over a period

        `<https://www.elastic.co/guide/en/app-search/current/counts.html>`_

        :param engine_name: Name of the engine
        :param filters:
        :param interval:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if filters is not None:
            __body["filters"] = filters
        if interval is not None:
            __body["interval"] = interval
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/analytics/counts",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def get_top_queries_analytics(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns queries analytics by usage count

        `<https://www.elastic.co/guide/en/app-search/current/queries.html#queries-top-queries>`_

        :param engine_name: Name of the engine
        :param current_page:
        :param filters:
        :param page_size:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if filters is not None:
            __body["filters"] = filters
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/analytics/queries",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def log_clickthrough(
        self,
        *,
        engine_name: str,
        document_id: str,
        query: str,
        request_id: t.Optional[str] = None,
        tags: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Tracks results that were clicked after a query

        `<https://www.elastic.co/guide/en/app-search/current/clickthrough.html>`_

        :param engine_name: Name of the engine
        :param document_id:
        :param query:
        :param request_id:
        :param tags:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if document_id is None:
            raise ValueError("Empty value passed for parameter 'document_id'")
        if query is None:
            raise ValueError("Empty value passed for parameter 'query'")
        __body: t.Dict[str, t.Any] = {}
        if document_id is not None:
            __body["document_id"] = document_id
        if query is not None:
            __body["query"] = query
        if request_id is not None:
            __body["request_id"] = request_id
        if tags is not None:
            __body["tags"] = tags
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/click",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def get_crawler_url_extraction_result(
        self,
        *,
        engine_name: str,
        body: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs an HTTP request to a given URL and extracts content from the page using
        standard App Search Crawler extraction pipeline.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-extract-url>`_

        :param engine_name: Name of the engine
        :param body:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/extract_url",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_crawler_crawl_request(
        self,
        *,
        engine_name: str,
        overrides: t.Mapping[str, t.Any],
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a request to perform a crawl of a given engine with the Crawler.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-crawl-requests>`_

        :param engine_name: Name of the engine
        :param overrides:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if overrides is None:
            raise ValueError("Empty value passed for parameter 'overrides'")
        __body: t.Dict[str, t.Any] = {}
        if overrides is not None:
            __body["overrides"] = overrides
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_requests",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_crawler_crawl_requests(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns a list of latest crawl requests for a given engine.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-crawl-requests>`_

        :param engine_name: Name of the engine
        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_requests",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_crawl_request(
        self,
        *,
        engine_name: str,
        crawl_request_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns crawl request details.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-crawl-requests-id>`_

        :param engine_name: Name of the engine
        :param crawl_request_id: Crawl Request ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if crawl_request_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'crawl_request_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_requests/{_quote(crawl_request_id)}",
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_active_crawl_request(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns active crawl request details.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-crawl-requests-active>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_requests/active",
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_crawler_active_crawl_request(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Cancels an active crawl request, stopping a running crawl if needed.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-crawl-requests-active-cancel>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_requests/active/cancel",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_crawler_crawl_rule(
        self,
        *,
        engine_name: str,
        domain_id: str,
        order: int,
        pattern: str,
        policy: t.Union["t.Literal['allow', 'deny']", str],
        rule: t.Union["t.Literal['begins', 'contains', 'ends', 'regex']", str],
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a crawl rule for a given engine and domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawl-rules>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param order:
        :param pattern:
        :param policy:
        :param rule:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if order is None:
            raise ValueError("Empty value passed for parameter 'order'")
        if pattern is None:
            raise ValueError("Empty value passed for parameter 'pattern'")
        if policy is None:
            raise ValueError("Empty value passed for parameter 'policy'")
        if rule is None:
            raise ValueError("Empty value passed for parameter 'rule'")
        __body: t.Dict[str, t.Any] = {}
        if order is not None:
            __body["order"] = order
        if pattern is not None:
            __body["pattern"] = pattern
        if policy is not None:
            __body["policy"] = policy
        if rule is not None:
            __body["rule"] = rule
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/crawl_rules",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_crawler_crawl_rule(
        self,
        *,
        engine_name: str,
        domain_id: str,
        crawl_rule_id: str,
        order: int,
        pattern: str,
        policy: t.Union["t.Literal['allow', 'deny']", str],
        rule: t.Union["t.Literal['begins', 'contains', 'ends', 'regex']", str],
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates crawl rule configuration

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-put-crawl-rule>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param crawl_rule_id: Crawl Rule ID
        :param order:
        :param pattern:
        :param policy:
        :param rule:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if crawl_rule_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'crawl_rule_id'")
        if order is None:
            raise ValueError("Empty value passed for parameter 'order'")
        if pattern is None:
            raise ValueError("Empty value passed for parameter 'pattern'")
        if policy is None:
            raise ValueError("Empty value passed for parameter 'policy'")
        if rule is None:
            raise ValueError("Empty value passed for parameter 'rule'")
        __body: t.Dict[str, t.Any] = {}
        if order is not None:
            __body["order"] = order
        if pattern is not None:
            __body["pattern"] = pattern
        if policy is not None:
            __body["policy"] = policy
        if rule is not None:
            __body["rule"] = rule
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/crawl_rules/{_quote(crawl_rule_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_crawler_crawl_rule(
        self,
        *,
        engine_name: str,
        domain_id: str,
        crawl_rule_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a crawl rule from a given domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-delete-crawl-rule>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param crawl_rule_id: Crawl Rule ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if crawl_rule_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'crawl_rule_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/crawl_rules/{_quote(crawl_rule_id)}",
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_crawl_schedule(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns the current crawl schedule for a given engine

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-crawl-schedule>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_schedule",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_crawler_crawl_schedule(
        self,
        *,
        engine_name: str,
        frequency: int,
        unit: t.Union["t.Literal['day', 'hour', 'month', 'week']", str],
    ) -> ObjectApiResponse[t.Any]:
        """
        Sets up a crawl schedule for a given engine

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-put-crawler-crawl-schedule>`_

        :param engine_name: Name of the engine
        :param frequency:
        :param unit:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if frequency is None:
            raise ValueError("Empty value passed for parameter 'frequency'")
        if unit is None:
            raise ValueError("Empty value passed for parameter 'unit'")
        __body: t.Dict[str, t.Any] = {}
        if frequency is not None:
            __body["frequency"] = frequency
        if unit is not None:
            __body["unit"] = unit
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_schedule",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_crawler_crawl_schedule(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a crawl schedule for a given engine

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-delete-crawler-crawl-schedule>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/crawl_schedule",
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_process_crawl_denied_urls(
        self,
        *,
        engine_name: str,
        process_crawl_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provides a sample list of urls identified for deletion by the given process crawl
        id.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-process-crawls-id-denied-urls>`_

        :param engine_name: Name of the engine
        :param process_crawl_id: Process Crawl identifier
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if process_crawl_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'process_crawl_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/process_crawls/{_quote(process_crawl_id)}/denied_urls",
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_crawler_domains(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns a list of crawler domains

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-domain>`_

        :param engine_name: Name of the engine
        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_crawler_domain(
        self,
        *,
        engine_name: str,
        crawl_rules: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        entry_points: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        name: t.Optional[str] = None,
        sitemaps: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a crawler domain configuration for a given engine

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-domains>`_

        :param engine_name: Name of the engine
        :param crawl_rules:
        :param entry_points:
        :param name:
        :param sitemaps:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if crawl_rules is not None:
            __body["crawl_rules"] = crawl_rules
        if entry_points is not None:
            __body["entry_points"] = entry_points
        if name is not None:
            __body["name"] = name
        if sitemaps is not None:
            __body["sitemaps"] = sitemaps
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_domain(
        self,
        *,
        engine_name: str,
        domain_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns crawler domain configuration details

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-domain>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_crawler_domain(
        self,
        *,
        engine_name: str,
        domain_id: str,
        crawl_rules: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        entry_points: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        name: t.Optional[str] = None,
        sitemaps: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates crawler domain configuration for a given domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-put-crawler-domain>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param crawl_rules:
        :param entry_points:
        :param name:
        :param sitemaps:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        __body: t.Dict[str, t.Any] = {}
        if crawl_rules is not None:
            __body["crawl_rules"] = crawl_rules
        if entry_points is not None:
            __body["entry_points"] = entry_points
        if name is not None:
            __body["name"] = name
        if sitemaps is not None:
            __body["sitemaps"] = sitemaps
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_crawler_domain(
        self,
        *,
        engine_name: str,
        domain_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes crawler domain configuration for a given domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-delete-crawler-domain>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_crawler_entry_point(
        self,
        *,
        engine_name: str,
        domain_id: str,
        value: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a crawler domain entry point for a given engine and domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-entry-points>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param value:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if value is None:
            raise ValueError("Empty value passed for parameter 'value'")
        __body: t.Dict[str, t.Any] = {}
        if value is not None:
            __body["value"] = value
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/entry_points",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_crawler_entry_point(
        self,
        *,
        engine_name: str,
        domain_id: str,
        entry_point_id: str,
        value: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates a crawler entry point with a new value

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-put-entry-point>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param entry_point_id: Crawler Entry Point identifier
        :param value:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if entry_point_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'entry_point_id'")
        if value is None:
            raise ValueError("Empty value passed for parameter 'value'")
        __body: t.Dict[str, t.Any] = {}
        if value is not None:
            __body["value"] = value
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/entry_points/{_quote(entry_point_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_crawler_entry_point(
        self,
        *,
        engine_name: str,
        domain_id: str,
        entry_point_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a crawler entry point

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-delete-crawler-domain>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param entry_point_id: Crawler Entry Point identifier
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if entry_point_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'entry_point_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/entry_points/{_quote(entry_point_id)}",
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_metrics(
        self,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a momentary snapshot of key crawler metrics, including global and node-level
        crawler health

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html>`_
        """
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/as/v1/crawler/metrics", headers=__headers
        )

    @_rewrite_parameters()
    def get_crawler_overview(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves crawler configuration overview of a given engine, including configured
        domains

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_crawler_process_crawl(
        self,
        *,
        engine_name: str,
        domains: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        dry_run: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Queues a task to reprocess crawled documents with current crawl configuration

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-process-crawls>`_

        :param engine_name: Name of the engine
        :param domains:
        :param dry_run:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if domains is not None:
            __body["domains"] = domains
        if dry_run is not None:
            __body["dry_run"] = dry_run
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/process_crawls",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_crawler_process_crawls(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns a list of latest process crawls for a given engine

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-process-crawls>`_

        :param engine_name: Name of the engine
        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/process_crawls",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_crawler_process_crawl(
        self,
        *,
        engine_name: str,
        process_crawl_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns process crawl details.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-get-crawler-process-crawls-id>`_

        :param engine_name: Name of the engine
        :param process_crawl_id: Process Crawl identifier
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if process_crawl_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'process_crawl_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/process_crawls/{_quote(process_crawl_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_crawler_sitemap(
        self,
        *,
        engine_name: str,
        domain_id: str,
        url: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a crawler sitemap configuration for a given engine and domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-sitemaps>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param url:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if url is None:
            raise ValueError("Empty value passed for parameter 'url'")
        __body: t.Dict[str, t.Any] = {}
        if url is not None:
            __body["url"] = url
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/sitemaps",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_crawler_sitemap(
        self,
        *,
        engine_name: str,
        domain_id: str,
        sitemap_id: str,
        url: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates sitemap configuration

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-put-sitemap>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param sitemap_id: Sitemap ID
        :param url:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if sitemap_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'sitemap_id'")
        if url is None:
            raise ValueError("Empty value passed for parameter 'url'")
        __body: t.Dict[str, t.Any] = {}
        if url is not None:
            __body["url"] = url
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/sitemaps/{_quote(sitemap_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_crawler_sitemap(
        self,
        *,
        engine_name: str,
        domain_id: str,
        sitemap_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a sitemap from a given domain

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-delete-sitemap>`_

        :param engine_name: Name of the engine
        :param domain_id: Crawler Domain ID
        :param sitemap_id: Sitemap ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if domain_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'domain_id'")
        if sitemap_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'sitemap_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/domains/{_quote(domain_id)}/sitemaps/{_quote(sitemap_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def get_crawler_url_tracing_result(
        self,
        *,
        engine_name: str,
        body: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns information about the history of a given URL with the App Search Crawler.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-trace-url>`_

        :param engine_name: Name of the engine
        :param body:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/trace_url",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def get_crawler_url_validation_result(
        self,
        *,
        engine_name: str,
        body: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs a number of checks on a given URL to make sure it is ready to be crawled
        and ingested into App Search.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-validate-url>`_

        :param engine_name: Name of the engine
        :param body:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/crawler/validate_url",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def get_crawler_domain_validation_result(
        self,
        *,
        body: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs a number of checks on a given domain name to make sure it is ready to
        be crawled and ingested into App Search.

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-post-crawler-validate-domain>`_

        :param body:
        """
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/as/v1/crawler/validate_url", body=__body, headers=__headers
        )

    @_rewrite_parameters()
    def get_crawler_user_agent(
        self,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves the currently configured value for the User-Agent header used for all
        Crawler HTTP requests

        `<https://www.elastic.co/guide/en/app-search/current/web-crawler-api-reference.html#web-crawler-apis-user-agent>`_
        """
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/as/v1/crawler/user_agent", headers=__headers
        )

    @_rewrite_parameters()
    def list_api_keys(
        self,
        *,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        List the details of all API keys

        `<https://www.elastic.co/guide/en/app-search/current/credentials.html#credentials-all>`_

        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/as/v1/credentials", params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_api_key(
        self,
        *,
        name: str,
        type: t.Union["t.Literal['admin', 'private', 'search']", str],
        access_all_engines: t.Optional[bool] = None,
        engines: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        read: t.Optional[bool] = None,
        write: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates an App Search API key

        `<https://www.elastic.co/guide/en/app-search/current/credentials.html#credentials-create>`_

        :param name:
        :param type:
        :param access_all_engines:
        :param engines:
        :param read:
        :param write:
        """
        if name is None:
            raise ValueError("Empty value passed for parameter 'name'")
        if type is None:
            raise ValueError("Empty value passed for parameter 'type'")
        __body: t.Dict[str, t.Any] = {}
        if name is not None:
            __body["name"] = name
        if type is not None:
            __body["type"] = type
        if access_all_engines is not None:
            __body["access_all_engines"] = access_all_engines
        if engines is not None:
            __body["engines"] = engines
        if read is not None:
            __body["read"] = read
        if write is not None:
            __body["write"] = write
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/as/v1/credentials", body=__body, headers=__headers
        )

    @_rewrite_parameters()
    def get_api_key(
        self,
        *,
        api_key_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves details of an API key

        `<https://www.elastic.co/guide/en/app-search/current/credentials.html#credentials-single>`_

        :param api_key_name: Name of an API key
        """
        if api_key_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'api_key_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", f"/api/as/v1/credentials/{_quote(api_key_name)}", headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_api_key(
        self,
        *,
        api_key_name: str,
        name: str,
        type: t.Union["t.Literal['admin', 'private', 'search']", str],
        access_all_engines: t.Optional[bool] = None,
        engines: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        read: t.Optional[bool] = None,
        write: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates an API key

        `<https://www.elastic.co/guide/en/app-search/current/credentials.html#credentials-update>`_

        :param api_key_name: Name of an API key
        :param name:
        :param type:
        :param access_all_engines:
        :param engines:
        :param read:
        :param write:
        """
        if api_key_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'api_key_name'")
        if name is None:
            raise ValueError("Empty value passed for parameter 'name'")
        if type is None:
            raise ValueError("Empty value passed for parameter 'type'")
        __body: t.Dict[str, t.Any] = {}
        if name is not None:
            __body["name"] = name
        if type is not None:
            __body["type"] = type
        if access_all_engines is not None:
            __body["access_all_engines"] = access_all_engines
        if engines is not None:
            __body["engines"] = engines
        if read is not None:
            __body["read"] = read
        if write is not None:
            __body["write"] = write
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/credentials/{_quote(api_key_name)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_api_key(
        self,
        *,
        api_key_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a given API key

        `<https://www.elastic.co/guide/en/app-search/current/credentials.html#credentials-destroy>`_

        :param api_key_name: Name of an API key
        """
        if api_key_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'api_key_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/credentials/{_quote(api_key_name)}",
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_curations(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve available curations for the given engine

        `<https://www.elastic.co/guide/en/app-search/current/curations.html#curations-read>`_

        :param engine_name: Name of the engine
        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/curations",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_curation(
        self,
        *,
        engine_name: str,
        queries: t.Union[t.List[str], t.Tuple[str, ...]],
        hidden: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        promoted: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        suggestion: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Create a new curation for the engine

        `<https://www.elastic.co/guide/en/app-search/current/curations.html#curations-create>`_

        :param engine_name: Name of the engine
        :param queries:
        :param hidden:
        :param promoted:
        :param suggestion:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if queries is None:
            raise ValueError("Empty value passed for parameter 'queries'")
        __body: t.Dict[str, t.Any] = {}
        if queries is not None:
            __body["queries"] = queries
        if hidden is not None:
            __body["hidden"] = hidden
        if promoted is not None:
            __body["promoted"] = promoted
        if suggestion is not None:
            __body["suggestion"] = suggestion
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/curations",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_curation(
        self,
        *,
        engine_name: str,
        curation_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a curation by ID

        `<https://www.elastic.co/guide/en/app-search/current/curations.html#curations-read>`_

        :param engine_name: Name of the engine
        :param curation_id: Curation ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if curation_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'curation_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/curations/{_quote(curation_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_curation(
        self,
        *,
        engine_name: str,
        curation_id: str,
        queries: t.Union[t.List[str], t.Tuple[str, ...]],
        hidden: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        promoted: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        suggestion: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates an existing curation

        `<https://www.elastic.co/guide/en/app-search/current/curations.html#curations-update>`_

        :param engine_name: Name of the engine
        :param curation_id: Curation ID
        :param queries:
        :param hidden:
        :param promoted:
        :param suggestion:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if curation_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'curation_id'")
        if queries is None:
            raise ValueError("Empty value passed for parameter 'queries'")
        __body: t.Dict[str, t.Any] = {}
        if queries is not None:
            __body["queries"] = queries
        if hidden is not None:
            __body["hidden"] = hidden
        if promoted is not None:
            __body["promoted"] = promoted
        if suggestion is not None:
            __body["suggestion"] = suggestion
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/curations/{_quote(curation_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_curation(
        self,
        *,
        engine_name: str,
        curation_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a curation set by ID

        `<https://www.elastic.co/guide/en/app-search/current/curations.html#curations-destroy>`_

        :param engine_name: Name of the engine
        :param curation_id: Curation ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if curation_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'curation_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/curations/{_quote(curation_id)}",
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_documents(
        self,
        *,
        engine_name: str,
        document_ids: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves one or more documents by id

        `<https://www.elastic.co/guide/en/app-search/current/documents.html#documents-get>`_

        :param engine_name: Name of the engine
        :param document_ids: List of Document IDs to fetch
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if document_ids is not None:
            __query["ids[]"] = document_ids
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/documents",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="documents",
    )
    def index_documents(
        self,
        *,
        engine_name: str,
        documents: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Create or update documents

        `<https://www.elastic.co/guide/en/app-search/current/documents.html#documents-create>`_

        :param engine_name: Name of the engine
        :param documents:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if documents is not None:
            __body = documents
        else:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/documents",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="document_ids",
    )
    def delete_documents(
        self,
        *,
        engine_name: str,
        document_ids: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes documents for given Document IDs

        `<https://www.elastic.co/guide/en/app-search/current/documents.html#documents-delete>`_

        :param engine_name: Name of the engine
        :param document_ids:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if document_ids is not None:
            __body = document_ids
        else:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/documents",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="documents",
    )
    def put_documents(
        self,
        *,
        engine_name: str,
        documents: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Update specific document fields by id and field

        `<https://www.elastic.co/guide/en/app-search/current/documents.html#documents-partial>`_

        :param engine_name: Name of the engine
        :param documents:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if documents is not None:
            __body = documents
        else:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PATCH",
            f"/api/as/v1/engines/{_quote(engine_name)}/documents",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_documents(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Lists up to 10,000 documents

        `<https://www.elastic.co/guide/en/app-search/current/documents.html#documents-list>`_

        :param engine_name: Name of the engine
        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/documents/list",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_engines(
        self,
        *,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves all engines with optional pagination support

        `<https://www.elastic.co/guide/en/app-search/current/engines.html#engines-list>`_

        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/as/v1/engines", params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_engine(
        self,
        *,
        engine_name: str,
        index_create_settings_override: t.Optional[t.Mapping[str, t.Any]] = None,
        language: t.Optional[
            t.Union[
                "t.Literal['da', 'de', 'en', 'es', 'fr', 'it', 'ja', 'ko', 'nl', 'pt', 'pt-br', 'ru', 'th', 'zh']",
                str,
            ]
        ] = None,
        source_engines: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        type: t.Optional[t.Union["t.Literal['default', 'meta']", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates an App Search Engine

        `<https://www.elastic.co/guide/en/app-search/current/engines.html#engines-create>`_

        :param engine_name:
        :param index_create_settings_override:
        :param language:
        :param source_engines:
        :param type:
        """
        if engine_name is None:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if engine_name is not None:
            __body["name"] = engine_name
        if index_create_settings_override is not None:
            __body["index_create_settings_override"] = index_create_settings_override
        if language is not None:
            __body["language"] = language
        if source_engines is not None:
            __body["source_engines"] = source_engines
        if type is not None:
            __body["type"] = type
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/as/v1/engines", body=__body, headers=__headers
        )

    @_rewrite_parameters()
    def get_engine(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves details of a given engine by its name

        `<https://www.elastic.co/guide/en/app-search/current/engines.html#engines-get>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", f"/api/as/v1/engines/{_quote(engine_name)}", headers=__headers
        )

    @_rewrite_parameters()
    def delete_engine(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Delete an engine by name

        `<https://www.elastic.co/guide/en/app-search/current/engines.html#engines-delete>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", f"/api/as/v1/engines/{_quote(engine_name)}", headers=__headers
        )

    @_rewrite_parameters(
        body_name="source_engines",
    )
    def delete_meta_engine_source(
        self,
        *,
        engine_name: str,
        source_engines: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a source engine from a given meta engine

        `<https://www.elastic.co/guide/en/app-search/current/meta-engines.html#meta-engines-remove-source-engines>`_

        :param engine_name: Name of the engine
        :param source_engines:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if source_engines is not None:
            __body = source_engines
        else:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/source_engines",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="source_engines",
    )
    def add_meta_engine_source(
        self,
        *,
        engine_name: str,
        source_engines: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Adds a source engine to a given meta engine

        `<https://www.elastic.co/guide/en/app-search/current/meta-engines.html#meta-engines-add-source-engines>`_

        :param engine_name: Name of the engine
        :param source_engines:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if source_engines is not None:
            __body = source_engines
        else:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/source_engines",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def get_api_logs(
        self,
        *,
        engine_name: str,
        filters: t.Mapping[str, t.Any],
        page: t.Optional[t.Mapping[str, t.Any]] = None,
        query: t.Optional[str] = None,
        sort_direction: t.Optional[t.Union["t.Literal['asc', 'desc']", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        The API Log displays API request and response data at the Engine level

        `<https://www.elastic.co/guide/en/app-search/current/api-logs.html>`_

        :param engine_name: Name of the engine
        :param filters:
        :param page:
        :param query:
        :param sort_direction:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if filters is None:
            raise ValueError("Empty value passed for parameter 'filters'")
        __body: t.Dict[str, t.Any] = {}
        if filters is not None:
            __body["filters"] = filters
        if page is not None:
            __body["page"] = page
        if query is not None:
            __body["query"] = query
        if sort_direction is not None:
            __body["sort_direction"] = sort_direction
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/logs/api",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def query_suggestion(
        self,
        *,
        engine_name: str,
        query: t.Optional[str] = None,
        size: t.Optional[int] = None,
        types: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provide relevant query suggestions for incomplete queries

        `<https://www.elastic.co/guide/en/app-search/current/query-suggestion.html>`_

        :param engine_name: Name of the engine
        :param query:
        :param size:
        :param types:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if query is not None:
            __body["query"] = query
        if size is not None:
            __body["size"] = size
        if types is not None:
            __body["types"] = types
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/query_suggestion",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_schema(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve current schema for the engine

        `<https://www.elastic.co/guide/en/app-search/current/schema.html#schema-read>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", f"/api/as/v1/engines/{_quote(engine_name)}/schema", headers=__headers
        )

    @_rewrite_parameters(
        body_name="schema",
    )
    def put_schema(
        self,
        *,
        engine_name: str,
        schema: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Update schema for the current engine

        `<https://www.elastic.co/guide/en/app-search/current/schema.html#schema-patch>`_

        :param engine_name: Name of the engine
        :param schema:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if schema is not None:
            __body = schema
        else:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/schema",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def search(
        self,
        *,
        engine_name: str,
        query: str,
        analytics: t.Optional[t.Mapping[str, t.Any]] = None,
        boost: t.Optional[t.Mapping[str, t.Any]] = None,
        current_page: t.Optional[int] = None,
        facets: t.Optional[t.Mapping[str, t.Any]] = None,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        group: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
        result_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        search_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        sort: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Submit a search and receive a set of results with meta data

        `<https://www.elastic.co/guide/en/app-search/current/search.html>`_

        :param engine_name: Name of the engine
        :param query:
        :param analytics:
        :param boost:
        :param current_page:
        :param facets:
        :param filters:
        :param group:
        :param page_size:
        :param result_fields:
        :param search_fields:
        :param sort:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if query is None:
            raise ValueError("Empty value passed for parameter 'query'")
        __body: t.Dict[str, t.Any] = {}
        if query is not None:
            __body["query"] = query
        if analytics is not None:
            __body["analytics"] = analytics
        if boost is not None:
            __body["boosts"] = boost
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if facets is not None:
            __body["facets"] = facets
        if filters is not None:
            __body["filters"] = filters
        if group is not None:
            __body["group"] = group
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        if result_fields is not None:
            __body["result_fields"] = result_fields
        if search_fields is not None:
            __body["search_fields"] = search_fields
        if sort is not None:
            __body["sort"] = sort
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/search",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def multi_search(
        self,
        *,
        engine_name: str,
        queries: t.Union[
            t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
        ],
    ) -> ObjectApiResponse[t.Any]:
        """
        Submit a multi search query and receive a set of results with meta data

        `<https://www.elastic.co/guide/en/app-search/current/multi-search.html>`_

        :param engine_name: Name of the engine
        :param queries:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if queries is None:
            raise ValueError("Empty value passed for parameter 'queries'")
        __body: t.Dict[str, t.Any] = {}
        if queries is not None:
            __body["queries"] = queries
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/multi_search",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def search_explain(
        self,
        *,
        engine_name: str,
        query: str,
        analytics: t.Optional[t.Mapping[str, t.Any]] = None,
        boost: t.Optional[t.Mapping[str, t.Any]] = None,
        current_page: t.Optional[int] = None,
        facets: t.Optional[t.Mapping[str, t.Any]] = None,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
        group: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
        result_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        search_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        sort: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Submit a search and retrieve an Elasticsearch query

        `<https://www.elastic.co/guide/en/app-search/current/search-explain.html>`_

        :param engine_name: Name of the engine
        :param query:
        :param analytics:
        :param boost:
        :param current_page:
        :param facets:
        :param filters:
        :param group:
        :param page_size:
        :param result_fields:
        :param search_fields:
        :param sort:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if query is None:
            raise ValueError("Empty value passed for parameter 'query'")
        __body: t.Dict[str, t.Any] = {}
        if query is not None:
            __body["query"] = query
        if analytics is not None:
            __body["analytics"] = analytics
        if boost is not None:
            __body["boosts"] = boost
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if facets is not None:
            __body["facets"] = facets
        if filters is not None:
            __body["filters"] = filters
        if group is not None:
            __body["group"] = group
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        if result_fields is not None:
            __body["result_fields"] = result_fields
        if search_fields is not None:
            __body["search_fields"] = search_fields
        if sort is not None:
            __body["sort"] = sort
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v0/engines/{_quote(engine_name)}/search_explain",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_search_settings(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve current search settings for the engine

        `<https://www.elastic.co/guide/en/app-search/current/search-settings.html#search-settings-show>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/search_settings",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_search_settings(
        self,
        *,
        engine_name: str,
        boosts: t.Optional[t.Mapping[str, t.Any]] = None,
        precision: t.Optional[int] = None,
        result_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        search_fields: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates search settings for the engine

        `<https://www.elastic.co/guide/en/app-search/current/search-settings.html#search-settings-update>`_

        :param engine_name: Name of the engine
        :param boosts:
        :param precision:
        :param result_fields:
        :param search_fields:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __body: t.Dict[str, t.Any] = {}
        if boosts is not None:
            __body["boosts"] = boosts
        if precision is not None:
            __body["precision"] = precision
        if result_fields is not None:
            __body["result_fields"] = result_fields
        if search_fields is not None:
            __body["search_fields"] = search_fields
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/search_settings",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def reset_search_settings(
        self,
        *,
        engine_name: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Resets search settings for the engine

        `<https://www.elastic.co/guide/en/app-search/current/search-settings.html#search-settings-reset>`_

        :param engine_name: Name of the engine
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/search_settings/reset",
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_synonym_sets(
        self,
        *,
        engine_name: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves all available synonym sets for the engine

        `<https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-get>`_

        :param engine_name: Name of the engine
        :param current_page: The page to fetch. Defaults to 1
        :param page_size: The number of results per page
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/synonyms",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_synonym_set(
        self,
        *,
        engine_name: str,
        synonyms: t.Union[t.List[str], t.Tuple[str, ...]],
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a new synonym set for the engine

        `<https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-create>`_

        :param engine_name: Name of the engine
        :param synonyms:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if synonyms is None:
            raise ValueError("Empty value passed for parameter 'synonyms'")
        __body: t.Dict[str, t.Any] = {}
        if synonyms is not None:
            __body["synonyms"] = synonyms
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/as/v1/engines/{_quote(engine_name)}/synonyms",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_synonym_set(
        self,
        *,
        engine_name: str,
        synonym_set_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a synonym set by ID

        `<https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-list-one>`_

        :param engine_name: Name of the engine
        :param synonym_set_id: Synonym Set ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'synonym_set_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/as/v1/engines/{_quote(engine_name)}/synonyms/{_quote(synonym_set_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_synonym_set(
        self,
        *,
        engine_name: str,
        synonym_set_id: str,
        synonyms: t.Union[t.List[str], t.Tuple[str, ...]],
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates a synonym set by ID

        `<https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-update>`_

        :param engine_name: Name of the engine
        :param synonym_set_id: Synonym Set ID
        :param synonyms:
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'synonym_set_id'")
        if synonyms is None:
            raise ValueError("Empty value passed for parameter 'synonyms'")
        __body: t.Dict[str, t.Any] = {}
        if synonyms is not None:
            __body["synonyms"] = synonyms
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/as/v1/engines/{_quote(engine_name)}/synonyms/{_quote(synonym_set_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_synonym_set(
        self,
        *,
        engine_name: str,
        synonym_set_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a synonym set by ID

        `<https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-delete>`_

        :param engine_name: Name of the engine
        :param synonym_set_id: Synonym Set ID
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'engine_name'")
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'synonym_set_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/as/v1/engines/{_quote(engine_name)}/synonyms/{_quote(synonym_set_id)}",
            headers=__headers,
        )
