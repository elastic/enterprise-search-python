from ._components import DocumentBulkCreateResponse, DocumentBulkDeleteResponse
from .utils import make_path


class WorkplaceSearch(object):
    # AUTO-GENERATED-API-DEFINITIONS #
    def index_documents(
        self, content_source_key, body, params=None, headers=None,
    ):
        # type: (...) -> DocumentBulkCreateResponse
        """
        Indexes one or more new documents into a custom content source, or updates one
        or more existing documents


        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#index-and-update>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        """
        return DocumentBulkCreateResponse(
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

    def delete_documents(
        self, content_source_key, body, params=None, headers=None,
    ):
        # type: (...) -> DocumentBulkDeleteResponse
        """
        Deletes a list of documents from a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#destroy>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        """
        return DocumentBulkDeleteResponse(
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
        page_current=None,
        page_size=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> ListAllExternalIdentitiesResponse
        """
        Retrieves all external identities

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#list-external-identities>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg page_current: Which page of results to request
        :arg page_size: The number of results to return in a page
        """
        return ListAllExternalIdentitiesResponse(
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
        # type: (...) -> ExternalIdentity
        """
        Adds a new external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#add-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        """
        return ExternalIdentity(
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

    def show_external_identity(
        self, content_source_key, user, params=None, headers=None,
    ):
        # type: (...) -> ExternalIdentity
        """
        Retrieves an external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#show-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg user: The username in context
        """
        return ExternalIdentity(
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

    def update_external_identity(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> ExternalIdentity
        """
        Updates an external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#update-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg user: The username in context
        """
        return ExternalIdentity(
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

    def delete_external_identity(
        self, content_source_key, user, params=None, headers=None,
    ):
        # type: (...) -> DeleteExternalIdentitiesResponse
        """
        Deletes an external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#remove-external-identity>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg user: The username in context
        """
        return DeleteExternalIdentitiesResponse(
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

    def list_all_permissions(
        self,
        content_source_key,
        page_current=None,
        page_size=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> ListAllPermissionsResponse
        """
        Lists all permissions for all users

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#list>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg page_current: Which page of results to request
        :arg page_size: The number of results to return in a page
        """
        return ListAllPermissionsResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "ws", "v1", "sources", content_source_key, "permissions",
                ),
                params=params,
                headers=headers,
            )
        )

    def get_user_permissions(
        self, content_source_key, user, params=None, headers=None,
    ):
        # type: (...) -> PermissionsUser
        """
        Lists all permissions for one user

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#list-one>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg user: The username in context
        """
        return PermissionsUser(
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

    def update_user_permissions(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> PermissionsUser
        """
        Creates a new set of permissions or over-writes all existing permissions

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#add-all>`_

        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source
        :arg user: The username in context
        """
        return PermissionsUser(
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
                ),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def add_user_permissions(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> PermissionsUser
        """
        Adds one or more new permissions atop existing permissions


        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#add-one>`_





        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source


        :arg user: The username in context


        """
        return PermissionsUser(
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

    def remove_user_permissions(
        self, content_source_key, user, body, params=None, headers=None,
    ):
        # type: (...) -> PermissionsUser
        """
        Removes one or more permissions from an existing set of permissions


        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#remove-one>`_





        :arg content_source_key: Unique key for a Custom API source,
            provided upon creation of a Custom API Source


        :arg user: The username in context


        """
        return PermissionsUser(
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
