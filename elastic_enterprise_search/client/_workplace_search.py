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

from elastic_transport import QueryParams

from .._utils import (  # noqa: F401
    DEFAULT,
    SKIP_IN_PATH,
    to_array,
    to_deep_object,
    to_path,
)
from ._base import BaseClient


class WorkplaceSearch(BaseClient):
    def create_analytics_event(
        self,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Capture click and feedback analytic events

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-analytics-api.html>`_

        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            "/api/ws/v1/analytics/event",
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_auto_query_refinement_details(
        self,
        content_source_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves a content source's automatic query refinement details

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#get-automatic-query-refinement-details-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "automatic_query_refinement",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def create_batch_synonym_sets(
        self,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Create a batch of synonym sets

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#create-synonyms>`_

        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            "/api/ws/v1/synonyms",
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def command_sync_jobs(
        self,
        content_source_id,
        body,
        job_type=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Issue commands to a Content Source's sync jobs

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-sync-jobs-api.html#command-sync-jobs-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg job_type: The type of sync job to consider
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.PaymentRequiredError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)
        if job_type is not None:
            for v in to_array(job_type, param="job_type"):
                params.add("job_type[]", v)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "sync",
                "jobs",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def create_content_source(
        self,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Create a content source

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#create-content-source-api>`_

        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            "/api/ws/v1/sources",
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_content_source(
        self,
        content_source_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Deletes a content source by ID

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#remove-content-source-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "DELETE",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_content_source(
        self,
        content_source_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves a content source by ID

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#get-content-source-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_content_source_icons(
        self,
        content_source_id,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Upload content source icons

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#upload-content-source-icon-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "PUT",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "icon",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_content_source(
        self,
        content_source_id,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update a content source

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#update-content-source-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "PUT",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_content_sources(
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
        Retrieves all content sources

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#list-content-sources-api>`_

        :arg current_page: Which page of results to request
        :arg page_size: The number of results to return in a page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """

        params = QueryParams(params)
        if current_page is not None:
            params.add("page[current]", current_page)
        if page_size is not None:
            params.add("page[size]", page_size)

        return self.perform_request(
            "GET",
            "/api/ws/v1/sources",
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_current_user(
        self,
        get_token=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Get the authenticated user

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-user-api.html#get-current-user-api>`_

        :arg get_token: Whether or not to include an access token in the
            response.
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """

        params = QueryParams(params)
        if get_token is not None:
            params.add("get_token", get_token)

        return self.perform_request(
            "GET",
            "/api/ws/v1/whoami",
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_document(
        self,
        content_source_id,
        document_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves a document by ID from the specified content source

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-content-sources-api.html#get-document-by-id-api>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg document_id: Unique ID for a content source document. Provided upon
            or returned at creation.
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            document_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "documents",
                document_id,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_documents_by_query(
        self,
        content_source_id,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Deletes documents by query in a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-custom-sources-api.html#delete-documents-by-query>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "DELETE",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "documents",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_documents(
        self,
        content_source_id,
        document_ids,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Deletes a list of documents from a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-custom-sources-api.html#delete-by-id>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg document_ids: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        :raises elastic_enterprise_search.PayloadTooLargeError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "documents",
                "bulk_destroy",
            ),
            body=document_ids,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def index_documents(
        self,
        content_source_id,
        documents,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Indexes one or more new documents into a custom content source, or updates one
        or more existing documents

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-custom-sources-api.html#index-and-update>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg documents: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        :raises elastic_enterprise_search.PayloadTooLargeError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "documents",
                "bulk_create",
            ),
            body=documents,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_documents(
        self,
        content_source_id,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Lists documents from a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-custom-sources-api.html#list-documents>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "documents",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_external_identities(
        self,
        content_source_id,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves all external identities

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-external-identities-api.html#list-external-identities>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg current_page: Which page of results to request
        :arg page_size: The number of results to return in a page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)
        if current_page is not None:
            params.add("page[current]", current_page)
        if page_size is not None:
            params.add("page[size]", page_size)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "external_identities",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def create_external_identity(
        self,
        content_source_id,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Adds a new external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-external-identities-api.html#add-external-identity>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "external_identities",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_external_identity(
        self,
        content_source_id,
        user,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Deletes an external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-external-identities-api.html#remove-external-identity>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "DELETE",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "external_identities",
                user,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_external_identity(
        self,
        content_source_id,
        user,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves an external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-external-identities-api.html#show-external-identity>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "external_identities",
                user,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_external_identity(
        self,
        content_source_id,
        user,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Updates an external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-external-identities-api.html#update-external-identity>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "PUT",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "external_identities",
                user,
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_permissions(
        self,
        content_source_id,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Lists all permissions for all users

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-document-permissions-api.html#list>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg current_page: Which page of results to request
        :arg page_size: The number of results to return in a page
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.PaymentRequiredError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)
        if current_page is not None:
            params.add("page[current]", current_page)
        if page_size is not None:
            params.add("page[size]", page_size)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "permissions",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def remove_user_permissions(
        self,
        content_source_id,
        user,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Removes one or more permissions from an existing set of permissions

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-document-permissions-api.html#remove-one>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.PaymentRequiredError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "permissions",
                user,
                "remove",
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
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Search across available sources with various query tuning options

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-search-api.html>`_

        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            "/api/ws/v1/search",
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def delete_synonym_set(
        self,
        synonym_set_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Delete a synonym set

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#delete-synonym>`_

        :arg synonym_set_id: Synonym Set ID
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "DELETE",
            to_path(
                "api",
                "ws",
                "v1",
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
        synonym_set_id,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieve a synonym set by ID

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#show-synonym>`_

        :arg synonym_set_id: Synonym Set ID
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
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
        synonym_set_id,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update a synonym set

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#update-synonym>`_

        :arg synonym_set_id: Synonym Set ID
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "PUT",
            to_path(
                "api",
                "ws",
                "v1",
                "synonyms",
                synonym_set_id,
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def list_synonym_sets(
        self,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves all synonym sets

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#list-synonyms>`_

        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            "/api/ws/v1/synonyms",
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_triggers_blocklist(
        self,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Get current triggers blocklist

        `<https://www.elastic.co/guide/en/workplace-search/current/automatic-query-refinement-blocklist.html>`_

        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            "/api/ws/v1/automatic_query_refinement",
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_triggers_blocklist(
        self,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update current triggers blocklist

        `<https://www.elastic.co/guide/en/workplace-search/current/automatic-query-refinement-blocklist.html>`_

        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.NotFoundError:
        """

        params = QueryParams(params)

        return self.perform_request(
            "PUT",
            "/api/ws/v1/automatic_query_refinement",
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def add_user_permissions(
        self,
        content_source_id,
        user,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Adds one or more new permissions atop existing permissions

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-document-permissions-api.html#add-one>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.PaymentRequiredError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "POST",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "permissions",
                user,
                "add",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_user_permissions(
        self,
        content_source_id,
        user,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Lists all permissions for one user

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-document-permissions-api.html#list-one>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.PaymentRequiredError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "GET",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "permissions",
                user,
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_user_permissions(
        self,
        content_source_id,
        user,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Creates a new set of permissions or over-writes all existing permissions

        `<https://www.elastic.co/guide/en/workplace-search/7.17/workplace-search-document-permissions-api.html#add-all>`_

        :arg content_source_id: Unique ID for a Custom API source, provided upon
            creation of a Custom API Source
        :arg user: The username in context
        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.BadRequestError:
        :raises elastic_enterprise_search.UnauthorizedError:
        :raises elastic_enterprise_search.PaymentRequiredError:
        :raises elastic_enterprise_search.NotFoundError:
        """
        for param in (
            content_source_id,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = QueryParams(params)

        return self.perform_request(
            "PUT",
            to_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_id,
                "permissions",
                user,
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )
