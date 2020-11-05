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

from .._utils import DEFAULT, SKIP_IN_PATH, make_params, make_path  # noqa: F401
from ._base import BaseClient


class AppSearch(BaseClient):
    def get_api_logs(
        self,
        engine_name,
        from_date,
        to_date,
        current_page=None,
        page_size=None,
        query=None,
        http_status_filter=None,
        http_method_filter=None,
        sort_direction=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        The API Log displays API request and response data at the Engine level

        `<https://www.elastic.co/guide/en/app-search/7.10/api-logs.html>`_

        :arg engine_name: Name of the engine
        :arg from_date: Filter date from
        :arg to_date: Filter date to
        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg query: Use this to specify a particular endpoint, like analytics,
            search, curations and so on
        :arg http_status_filter: Filter based on a particular status code: 400,
            401, 403, 429, 200
        :arg http_method_filter: Filter based on a particular HTTP method: GET,
            POST, PUT, PATCH, DELETE
        :arg sort_direction: Would you like to have your results ascending,
            oldest to newest, or descending, newest to oldest?
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            from_date,
            to_date,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "filters[date][from]": from_date,
                "filters[date][to]": to_date,
                "page[current]": current_page,
                "page[size]": page_size,
                "query": query,
                "filters[status]": http_status_filter,
                "filters[method]": http_method_filter,
                "sort_direction": sort_direction,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "logs",
                "api",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_count_analytics(
        self,
        engine_name,
        filters=None,
        interval=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Returns the number of clicks and total number of queries over a period

        `<https://www.elastic.co/guide/en/app-search/7.10/counts.html>`_

        :arg engine_name: Name of the engine
        :arg filters: Analytics filters
        :arg interval: You can define an interval along with your date range.
            Can be either hour or day
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "filters": filters,
                "interval": interval,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "analytics",
                "counts",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def create_curation(
        self,
        engine_name,
        queries,
        promoted_doc_ids=None,
        hidden_doc_ids=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Create a new curation

        `<https://www.elastic.co/guide/en/app-search/7.10/curations.html#curations-create>`_

        :arg engine_name: Name of the engine
        :arg queries: List of affected search queries
        :arg promoted_doc_ids: List of promoted document IDs
        :arg hidden_doc_ids: List of hidden document IDs
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            queries,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "queries": queries,
                "promoted": promoted_doc_ids,
                "hidden": hidden_doc_ids,
            },
        )
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "curations",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_curation(
        self,
        engine_name,
        curation_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Delete a curation by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/curations.html#curations-destroy>`_

        :arg engine_name: Name of the engine
        :arg curation_id: Curation ID
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            curation_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "DELETE",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "curations",
                curation_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_curation(
        self,
        engine_name,
        curation_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieve a curation by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/curations.html#curations-read>`_

        :arg engine_name: Name of the engine
        :arg curation_id: Curation ID
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            curation_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "curations",
                curation_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_curation(
        self,
        engine_name,
        curation_id,
        queries,
        promoted_doc_ids=None,
        hidden_doc_ids=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update an existing curation

        `<https://www.elastic.co/guide/en/app-search/7.10/curations.html#curations-update>`_

        :arg engine_name: Name of the engine
        :arg curation_id: Curation ID
        :arg queries: List of affected search queries
        :arg promoted_doc_ids: List of promoted document IDs
        :arg hidden_doc_ids: List of hidden document IDs
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            curation_id,
            queries,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "queries": queries,
                "promoted": promoted_doc_ids,
                "hidden": hidden_doc_ids,
            },
        )
        return self.perform_request(
            "PUT",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "curations",
                curation_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_curations(
        self,
        engine_name,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieve available curations for the engine

        `<https://www.elastic.co/guide/en/app-search/7.10/curations.html#curations-read>`_

        :arg engine_name: Name of the engine
        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "page[current]": current_page,
                "page[size]": page_size,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "curations",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_documents(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Delete documents by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/documents.html#documents-delete>`_

        :arg engine_name: Name of the engine
        :arg body: List of document IDs
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "DELETE",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "documents",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_documents(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves one or more documents by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/documents.html#documents-get>`_

        :arg engine_name: Name of the engine
        :arg body: List of document IDs
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "documents",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def index_documents(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Create or update documents

        `<https://www.elastic.co/guide/en/app-search/7.10/documents.html#documents-create>`_

        :arg engine_name: Name of the engine
        :arg body: List of document to index
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "documents",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_documents(
        self,
        engine_name,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        List all available documents with optional pagination support

        `<https://www.elastic.co/guide/en/app-search/7.10/documents.html#documents-list>`_

        :arg engine_name: Name of the engine
        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "page[current]": current_page,
                "page[size]": page_size,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "documents",
                "list",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_documents(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Partial update of documents

        `<https://www.elastic.co/guide/en/app-search/7.10/documents.html#documents-partial>`_

        :arg engine_name: Name of the engine
        :arg body: List of documents to update
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "PATCH",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "documents",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def create_engine(
        self,
        engine_name,
        language=None,
        type=None,
        source_engines=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Creates a new engine

        `<https://www.elastic.co/guide/en/app-search/7.10/engines.html#engines-create>`_

        :arg engine_name: Engine name
        :arg language: Engine language (null for universal)
        :arg type: Engine type
        :arg source_engines: Sources engines list
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "name": engine_name,
                "language": language,
                "type": type,
                "source_engines": source_engines,
            },
        )
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_engine(
        self,
        engine_name,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Delete an engine by name

        `<https://www.elastic.co/guide/en/app-search/7.10/engines.html#engines-delete>`_

        :arg engine_name: Name of the engine
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "DELETE",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_engine(
        self,
        engine_name,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves an engine by name

        `<https://www.elastic.co/guide/en/app-search/7.10/engines.html#engines-get>`_

        :arg engine_name: Name of the engine
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_engines(
        self,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves all engines with optional pagination support

        `<https://www.elastic.co/guide/en/app-search/7.10/engines.html#engines-list>`_

        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        params = make_params(
            params,
            {
                "page[current]": current_page,
                "page[size]": page_size,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def log_clickthrough(
        self,
        engine_name,
        query_text,
        document_id,
        request_id=None,
        tags=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Send data about clicked results

        `<https://www.elastic.co/guide/en/app-search/7.10/clickthrough.html>`_

        :arg engine_name: Name of the engine
        :arg query_text: Search query text
        :arg document_id: The ID of the document that was clicked on
        :arg request_id: The request ID returned in the meta tag of a search API
            response
        :arg tags: Array of strings representing additional information you wish
            to track with the clickthrough
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            query_text,
            document_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "query": query_text,
                "document_id": document_id,
                "request_id": request_id,
                "tags": tags,
            },
        )
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "click",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def add_meta_engine_source(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Add a source engine to an existing meta engine

        `<https://www.elastic.co/guide/en/app-search/7.10/meta-engines.html#meta-engines-add-source-engines>`_

        :arg engine_name: Name of the engine
        :arg body: List of engine IDs
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "source_engines",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_meta_engine_source(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Delete a source engine from a meta engine

        `<https://www.elastic.co/guide/en/app-search/7.10/meta-engines.html#meta-engines-remove-source-engines>`_

        :arg engine_name: Name of the engine
        :arg body: List of engine IDs
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "DELETE",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "source_engines",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def multi_search(
        self,
        engine_name,
        queries,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Run several search in the same request

        `<https://www.elastic.co/guide/en/app-search/7.10/search.html#search-multi>`_

        :arg engine_name: Name of the engine
        :arg queries: Search queries
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            queries,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "queries": queries,
            },
        )
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "multi_search",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def query_suggestion(
        self,
        engine_name,
        query,
        fields=None,
        size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Provide relevant query suggestions for incomplete queries

        `<https://www.elastic.co/guide/en/app-search/7.10/query-suggestion.html>`_

        :arg engine_name: Name of the engine
        :arg query: A partial query for which to receive suggestions
        :arg fields: List of fields to use to generate suggestions. Defaults to
            all text fields
        :arg size: Number of query suggestions to return. Must be between 1 and
            20. Defaults to 5
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            query,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "query": query,
                "types[documents][fields]": fields,
                "size": size,
            },
        )
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "query_suggestion",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_schema(
        self,
        engine_name,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieve current schema for then engine

        `<https://www.elastic.co/guide/en/app-search/7.10/schema.html#schema-read>`_

        :arg engine_name: Name of the engine
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "schema",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_schema(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update schema for the current engine

        `<https://www.elastic.co/guide/en/app-search/7.10/schema.html#schema-patch>`_

        :arg engine_name: Name of the engine
        :arg body: Schema description
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "schema",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def search(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Allows you to search over, facet and filter your data

        `<https://www.elastic.co/guide/en/app-search/7.10/search.html#search-single>`_

        :arg engine_name: Name of the engine
        :arg body: Search request parameters
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "search",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_search_settings(
        self,
        engine_name,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrive current search settings for the engine

        `<https://www.elastic.co/guide/en/app-search/7.10/search-settings.html#search-settings-show>`_

        :arg engine_name: Name of the engine
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "search_settings",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_search_settings(
        self,
        engine_name,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update search settings for the engine

        `<https://www.elastic.co/guide/en/app-search/7.10/search-settings.html#search-settings-update>`_

        :arg engine_name: Name of the engine
        :arg body: Search settings
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "PUT",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "search_settings",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def reset_search_settings(
        self,
        engine_name,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Reset search settings for the engine

        `<https://www.elastic.co/guide/en/app-search/7.10/search-settings.html#search-settings-reset>`_

        :arg engine_name: Name of the engine
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "search_settings",
                "reset",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def create_synonym_set(
        self,
        engine_name,
        synonyms,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Create a new synonym set

        `<https://www.elastic.co/guide/en/app-search/7.10/synonyms.html#synonyms-create>`_

        :arg engine_name: Name of the engine
        :arg synonyms: List of synonyms words
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            synonyms,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "synonyms": synonyms,
            },
        )
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "synonyms",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_synonym_set(
        self,
        engine_name,
        synonym_set_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Delete a synonym set by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/synonyms.html#synonyms-delete>`_

        :arg engine_name: Name of the engine
        :arg synonym_set_id: Synonym set ID
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            synonym_set_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "DELETE",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "synonyms",
                synonym_set_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_synonym_set(
        self,
        engine_name,
        synonym_set_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieve a synonym set by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/synonyms.html#synonyms-list-one>`_

        :arg engine_name: Name of the engine
        :arg synonym_set_id: Synonym set ID
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            synonym_set_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "synonyms",
                synonym_set_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_synonym_set(
        self,
        engine_name,
        synonym_set_id,
        synonyms,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update a synonym set by ID

        `<https://www.elastic.co/guide/en/app-search/7.10/synonyms.html#synonyms-update>`_

        :arg engine_name: Name of the engine
        :arg synonym_set_id: Synonym set ID
        :arg synonyms: List of synonyms words
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        for param in (
            engine_name,
            synonym_set_id,
            synonyms,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "synonyms": synonyms,
            },
        )
        return self.perform_request(
            "PUT",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "synonyms",
                synonym_set_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_synonym_sets(
        self,
        engine_name,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieve available synonym sets for the engine

        `<https://www.elastic.co/guide/en/app-search/7.10/synonyms.html#synonyms-get>`_

        :arg engine_name: Name of the engine
        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "page[current]": current_page,
                "page[size]": page_size,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "synonyms",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_top_clicks_analytics(
        self,
        engine_name,
        query=None,
        current_page=None,
        page_size=None,
        filters=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Returns the number of clicks received by a document in descending order

        `<https://www.elastic.co/guide/en/app-search/7.10/clicks.html>`_

        :arg engine_name: Name of the engine
        :arg query: Filter clicks over a search query
        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg filters: Analytics filters
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "query": query,
                "page[current]": current_page,
                "page[size]": page_size,
                "filters": filters,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "analytics",
                "clicks",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_top_queries_analytics(
        self,
        engine_name,
        current_page=None,
        page_size=None,
        filters=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Returns queries analytics by usage count

        `<https://www.elastic.co/guide/en/app-search/7.10/queries.html#queries-top-queries>`_

        :arg engine_name: Name of the engine
        :arg current_page: The page to fetch. Defaults to 1
        :arg page_size: The number of results per page
        :arg filters: Analytics filters
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        """
        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        params = make_params(
            params,
            {
                "page[current]": current_page,
                "page[size]": page_size,
                "filters": filters,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "as",
                "v1",
                "engines",
                engine_name,
                "analytics",
                "queries",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )
