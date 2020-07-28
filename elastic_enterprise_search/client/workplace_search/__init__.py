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

from ..utils import SKIP_IN_PATH, BaseClient, JSONResponse, make_path, make_params


class WorkplaceSearch(BaseClient):
    def delete_documents(
        self, content_source_key, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Deletes a list of documents from a custom content source
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        """

        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def list_all_external_identities(
        self,
        content_source_key,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieves all external identities
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg current_page: Which page of results to request
        :arg page_size: The number of results to return in a page
        """

        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"page[current]": current_page, "page[size]": page_size}
        )
        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def create_external_identity(
        self, content_source_key, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Adds a new external identity
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        """

        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def delete_external_identity(
        self, content_source_key, user, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Deletes an external identity
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def get_external_identity(
        self, content_source_key, user, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieves an external identity
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def put_external_identity(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Updates an external identity
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def index_documents(
        self, content_source_key, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Indexes one or more new documents into a custom content source, or updates one
        or more existing documents
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        """

        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def list_all_permissions(
        self,
        content_source_key,
        current_page=None,
        page_size=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Lists all permissions for all users
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg current_page: Which page of results to request
        :arg page_size: The number of results to return in a page
        """

        if content_source_key in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"page[current]": current_page, "page[size]": page_size}
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "ws", "v1", "sources", content_source_key, "permissions",
                ),
                params=params,
                headers=headers,
            )
        )

    def remove_user_permissions(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Removes one or more permissions from an existing set of permissions
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def search(
        self, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        search across available sources with various query tuning options
        
        """

        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "ws", "v1", "search"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def add_user_permissions(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Adds one or more new permissions atop existing permissions
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def get_user_permissions(
        self, content_source_key, user, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Lists all permissions for one user
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def put_user_permissions(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Creates a new set of permissions or over-writes all existing permissions
        
        :arg content_source_key: Unique key for a Custom API source, provided
            upon creation of a Custom API Source
        :arg user: The username in context
        """

        for param in (
            content_source_key,
            user,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )
