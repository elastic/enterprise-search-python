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


class WorkplaceSearch(BaseClient):
    def delete_documents(
        self,
        content_source_key,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Deletes a list of documents from a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-custom-sources-api.html#destroy>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
        :raises elastic_enterprise_search.PayloadTooLargeError:
        """
        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
                "documents",
                "bulk_destroy",
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
        content_source_key,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Indexes one or more new documents into a custom content source, or updates one
        or more existing documents

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-custom-sources-api.html#index-and-update>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
        :raises elastic_enterprise_search.PayloadTooLargeError:
        """
        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
                "documents",
                "bulk_create",
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
        content_source_key,
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

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-external-identities-api.html#list-external-identities>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
        if content_source_key in SKIP_IN_PATH:
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
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Adds a new external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-external-identities-api.html#add-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
        user,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Deletes an external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-external-identities-api.html#remove-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "DELETE",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
        user,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Retrieves an external identity

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-external-identities-api.html#show-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "GET",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
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

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-external-identities-api.html#update-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "PUT",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
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

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-document-permissions-api.html#list>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
        if content_source_key in SKIP_IN_PATH:
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
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
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

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-document-permissions-api.html#remove-one>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "POST",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        search across available sources with various query tuning options

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-search-api.html>`_

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
        return self.perform_request(
            "POST",
            make_path(
                "api",
                "ws",
                "v1",
                "search",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def add_user_permissions(
        self,
        content_source_key,
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

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-document-permissions-api.html#add-one>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "POST",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
        user,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Lists all permissions for one user

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-document-permissions-api.html#list-one>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "GET",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
        content_source_key,
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

        `<https://www.elastic.co/guide/en/workplace-search/7.10/workplace-search-document-permissions-api.html#add-all>`_

        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
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
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return self.perform_request(
            "PUT",
            make_path(
                "api",
                "ws",
                "v1",
                "sources",
                content_source_key,
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
