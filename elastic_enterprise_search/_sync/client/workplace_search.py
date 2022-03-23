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


class WorkplaceSearch(BaseClient):
    # AUTO-GENERATED-API-DEFINITIONS #

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_content_source(
        self,
        *,
        name: str,
        automatic_query_refinement: t.Optional[t.Mapping[str, t.Any]] = None,
        display: t.Optional[t.Mapping[str, t.Any]] = None,
        facets: t.Optional[t.Mapping[str, t.Any]] = None,
        indexing: t.Optional[t.Mapping[str, t.Any]] = None,
        is_searchable: t.Optional[bool] = None,
        schema: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Create a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#create-content-source-api>`_

        :param name:
        :param automatic_query_refinement:
        :param display:
        :param facets:
        :param indexing:
        :param is_searchable:
        :param schema:
        """
        if name is None:
            raise ValueError("Empty value passed for parameter 'name'")
        __body: t.Dict[str, t.Any] = {}
        if name is not None:
            __body["name"] = name
        if automatic_query_refinement is not None:
            __body["automatic_query_refinement"] = automatic_query_refinement
        if display is not None:
            __body["display"] = display
        if facets is not None:
            __body["facets"] = facets
        if indexing is not None:
            __body["indexing"] = indexing
        if is_searchable is not None:
            __body["is_searchable"] = is_searchable
        if schema is not None:
            __body["schema"] = schema
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/ws/v1/sources", body=__body, headers=__headers
        )

    @_rewrite_parameters()
    def list_content_sources(
        self,
        *,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves all content sources

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#list-content-sources-api>`_

        :param current_page: Which page of results to request
        :param page_size: The number of results to return in a page
        """
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ws/v1/sources", params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_content_source(
        self,
        *,
        content_source_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a content source by ID

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#get-content-source-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", f"/api/ws/v1/sources/{_quote(content_source_id)}", headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_content_source(
        self,
        *,
        content_source_id: str,
        is_searchable: bool,
        name: str,
        automatic_query_refinement: t.Optional[t.Mapping[str, t.Any]] = None,
        display: t.Optional[t.Mapping[str, t.Any]] = None,
        facets: t.Optional[t.Mapping[str, t.Any]] = None,
        indexing: t.Optional[t.Mapping[str, t.Any]] = None,
        schema: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Update a content source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#update-content-source-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param is_searchable:
        :param name:
        :param automatic_query_refinement:
        :param display:
        :param facets:
        :param indexing:
        :param schema:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if is_searchable is None:
            raise ValueError("Empty value passed for parameter 'is_searchable'")
        if name is None:
            raise ValueError("Empty value passed for parameter 'name'")
        __body: t.Dict[str, t.Any] = {}
        if is_searchable is not None:
            __body["is_searchable"] = is_searchable
        if name is not None:
            __body["name"] = name
        if automatic_query_refinement is not None:
            __body["automatic_query_refinement"] = automatic_query_refinement
        if display is not None:
            __body["display"] = display
        if facets is not None:
            __body["facets"] = facets
        if indexing is not None:
            __body["indexing"] = indexing
        if schema is not None:
            __body["schema"] = schema
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/ws/v1/sources/{_quote(content_source_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_content_source(
        self,
        *,
        content_source_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a content source by ID

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#remove-content-source-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/ws/v1/sources/{_quote(content_source_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_content_source_icons(
        self,
        *,
        content_source_id: str,
        alt_icon: t.Optional[str] = None,
        main_icon: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Upload content source icons

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#upload-content-source-icon-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param alt_icon:
        :param main_icon:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __body: t.Dict[str, t.Any] = {}
        if alt_icon is not None:
            __body["alt_icon"] = alt_icon
        if main_icon is not None:
            __body["main_icon"] = main_icon
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/icon",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def delete_documents_by_query(
        self,
        *,
        content_source_id: str,
        filters: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes documents by query in a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#delete-documents-by-query>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param filters:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __body: t.Dict[str, t.Any] = {}
        if filters is not None:
            __body["filters"] = filters
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/documents",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def list_documents(
        self,
        *,
        content_source_id: str,
        current_page: t.Optional[int] = None,
        cursor: t.Optional[str] = None,
        filters: t.Optional[t.Union[t.Any, t.Mapping[str, t.Any]]] = None,
        page_size: t.Optional[int] = None,
        sort: t.Optional[
            t.Union[
                t.Mapping[str, t.Any],
                t.Union[
                    t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
                ],
            ]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Lists documents from a custom content source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#list-documents>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param current_page:
        :param cursor:
        :param filters:
        :param page_size:
        :param sort:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __body: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if cursor is not None:
            __body["cursor"] = cursor
        if filters is not None:
            __body["filters"] = filters
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        if sort is not None:
            __body["sort"] = sort
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/documents",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="documents",
    )
    def index_documents(
        self,
        *,
        content_source_id: str,
        documents: t.Union[
            t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
        ],
    ) -> ObjectApiResponse[t.Any]:
        """
        Indexes one or more new documents into a custom content source, or updates one
        or more existing documents

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#index-and-update>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param documents:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if documents is None:
            raise ValueError("Empty value passed for parameter 'documents'")
        __body = documents
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/documents/bulk_create",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="document_ids",
    )
    def delete_documents(
        self,
        *,
        content_source_id: str,
        document_ids: t.Union[t.List[str], t.Tuple[str, ...]],
    ) -> ObjectApiResponse[t.Any]:
        """
        Remove documents from a Custom API Source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#delete-by-id>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param document_ids:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if document_ids is None:
            raise ValueError("Empty value passed for parameter 'document_ids'")
        __body = document_ids
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/documents/bulk_destroy",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_document(
        self,
        *,
        content_source_id: str,
        document_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a document by ID from the specified content source

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#get-document-by-id-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param document_id: Unique ID for a content source document. Provided upon or
            returned at creation.
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if document_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'document_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/documents/{_quote(document_id)}",
            headers=__headers,
        )

    @_rewrite_parameters()
    def list_external_identities(
        self,
        *,
        content_source_id: str,
        current_page: t.Optional[int] = None,
        page_size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves all external identities

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#list-external-identities>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param current_page: Which page of results to request
        :param page_size: The number of results to return in a page
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __query: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __query["page[current]"] = current_page
        if page_size is not None:
            __query["page[size]"] = page_size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/external_identities",
            params=__query,
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_external_identity(
        self,
        *,
        content_source_id: str,
        external_user_id: str,
        external_user_properties: t.Union[
            t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
        ],
        permissions: t.Union[t.List[str], t.Tuple[str, ...]],
    ) -> ObjectApiResponse[t.Any]:
        """
        Adds a new external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#add-external-identity>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param external_user_id:
        :param external_user_properties:
        :param permissions:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if external_user_id is None:
            raise ValueError("Empty value passed for parameter 'external_user_id'")
        if external_user_properties is None:
            raise ValueError(
                "Empty value passed for parameter 'external_user_properties'"
            )
        if permissions is None:
            raise ValueError("Empty value passed for parameter 'permissions'")
        __body: t.Dict[str, t.Any] = {}
        if external_user_id is not None:
            __body["external_user_id"] = external_user_id
        if external_user_properties is not None:
            __body["external_user_properties"] = external_user_properties
        if permissions is not None:
            __body["permissions"] = permissions
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/external_identities",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_external_identity(
        self,
        *,
        content_source_id: str,
        external_user_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves an external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#show-external-identity>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param external_user_id: Unique identifier of an external user, such as username
            or email address.
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if external_user_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'external_user_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/external_identities/{_quote(external_user_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_external_identity(
        self,
        *,
        content_source_id: str,
        external_user_id: str,
        external_user_properties: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        permissions: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates an external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#update-external-identity>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param external_user_id: Unique identifier of an external user, such as username
            or email address.
        :param external_user_properties:
        :param permissions:
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if external_user_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'external_user_id'")
        __body: t.Dict[str, t.Any] = {}
        if external_user_properties is not None:
            __body["external_user_properties"] = external_user_properties
        if permissions is not None:
            __body["permissions"] = permissions
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/external_identities/{_quote(external_user_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_external_identity(
        self,
        *,
        content_source_id: str,
        external_user_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes an external identity

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#remove-external-identity>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param external_user_id: Unique identifier of an external user, such as username
            or email address.
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if external_user_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'external_user_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/external_identities/{_quote(external_user_id)}",
            headers=__headers,
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def command_sync_jobs(
        self,
        *,
        content_source_id: str,
        body: t.Any,
        job_type: t.Optional[
            t.Union[
                t.List[
                    t.Union[
                        "t.Literal['delete', 'full', 'incremental', 'permissions']", str
                    ]
                ],
                t.Tuple[
                    t.Union[
                        "t.Literal['delete', 'full', 'incremental', 'permissions']", str
                    ],
                    ...,
                ],
            ]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Control a content source's sync jobs

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-sync-jobs-api.html#command-sync-jobs-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        :param body:
        :param job_type: The type of sync job to consider
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __query: t.Dict[str, t.Any] = {}
        if job_type is not None:
            __query["job_type"] = job_type
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/sync/jobs",
            params=__query,
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_synonym_set(
        self,
        *,
        synonym_set_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve a synonym set by ID

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#show-synonym>`_

        :param synonym_set_id: Synonym Set ID
        """
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'synonym_set_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", f"/api/ws/v1/synonyms/{_quote(synonym_set_id)}", headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_synonym_set(
        self,
        *,
        synonym_set_id: str,
        synonyms: t.Union[t.List[str], t.Tuple[str, ...]],
    ) -> ObjectApiResponse[t.Any]:
        """
        Update a synonym set

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#update-synonym>`_

        :param synonym_set_id: Synonym Set ID
        :param synonyms:
        """
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
            f"/api/ws/v1/synonyms/{_quote(synonym_set_id)}",
            body=__body,
            headers=__headers,
        )

    @_rewrite_parameters()
    def delete_synonym_set(
        self,
        *,
        synonym_set_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Delete a synonym set

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#delete-synonym>`_

        :param synonym_set_id: Synonym Set ID
        """
        if synonym_set_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'synonym_set_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", f"/api/ws/v1/synonyms/{_quote(synonym_set_id)}", headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def list_synonym_sets(
        self,
        *,
        current_page: t.Optional[int] = None,
        filter: t.Optional[t.Mapping[str, t.Any]] = None,
        page_size: t.Optional[int] = None,
        sort: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieve a list of synonym sets

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#list-synonyms>`_

        :param current_page:
        :param filter:
        :param page_size:
        :param sort:
        """
        __body: t.Dict[str, t.Any] = {}
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if filter is not None:
            __body["filter"] = filter
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        if sort is not None:
            __body["sort"] = sort
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ws/v1/synonyms", body=__body, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_batch_synonym_sets(
        self,
        *,
        synonym_sets: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        synonyms: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Create batched synonym sets

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-synonyms-api.html#create-synonyms>`_

        :param synonym_sets:
        :param synonyms:
        """
        __body: t.Dict[str, t.Any] = {}
        if synonym_sets is not None:
            __body["synonym_sets"] = synonym_sets
        if synonyms is not None:
            __body["synonyms"] = synonyms
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/ws/v1/synonyms", body=__body, headers=__headers
        )

    @_rewrite_parameters()
    def get_triggers_blocklist(
        self,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get current triggers blocklist

        `<https://www.elastic.co/guide/en/workplace-search/current/automatic-query-refinement-blocklist.html>`_
        """
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ws/v1/automatic_query_refinement", headers=__headers
        )

    @_rewrite_parameters()
    def put_triggers_blocklist(
        self,
    ) -> ObjectApiResponse[t.Any]:
        """
        Update current triggers blocklist

        `<https://www.elastic.co/guide/en/workplace-search/current/automatic-query-refinement-blocklist.html>`_
        """
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", "/api/ws/v1/automatic_query_refinement", headers=__headers
        )

    @_rewrite_parameters()
    def get_auto_query_refinement_details(
        self,
        *,
        content_source_id: str,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a content source's automatic query refinement details

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-content-sources-api.html#get-automatic-query-refinement-details-api>`_

        :param content_source_id: Unique ID for a Custom API source, provided upon creation
            of a Custom API Source
        """
        if content_source_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'content_source_id'")
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            f"/api/ws/v1/sources/{_quote(content_source_id)}/automatic_query_refinement",
            headers=__headers,
        )

    @_rewrite_parameters()
    def get_current_user(
        self,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get the authenticated user

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-user-api.html#get-current-user-api>`_
        """
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ws/v1/whoami", headers=__headers
        )

    @_rewrite_parameters(
        body_name="body",
    )
    def create_analytics_event(
        self,
        *,
        body: t.Any,
    ) -> ObjectApiResponse[t.Any]:
        """
        Capture Analytic events for click and feedback

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-analytics-api.html>`_

        :param body:
        """
        if body is None:
            raise ValueError("Empty value passed for parameter 'body'")
        __body = body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/ws/v1/analytics/event", body=__body, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def search(
        self,
        *,
        automatic_query_refinement: t.Optional[bool] = None,
        boosts: t.Optional[t.Mapping[str, t.Any]] = None,
        content_sources: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        current_page: t.Optional[int] = None,
        facets: t.Optional[t.Mapping[str, t.Any]] = None,
        filters: t.Optional[t.Union[t.Any, t.Mapping[str, t.Any]]] = None,
        page_size: t.Optional[int] = None,
        query: t.Optional[str] = None,
        result_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        search_fields: t.Optional[t.Mapping[str, t.Any]] = None,
        sort: t.Optional[
            t.Union[
                t.Mapping[str, t.Any],
                t.Union[
                    t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
                ],
            ]
        ] = None,
        source_type: t.Optional[
            t.Union["t.Literal['all', 'remote', 'standard']", str]
        ] = None,
        timeout: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Issue a Search Query

        `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-search-api.html>`_

        :param automatic_query_refinement:
        :param boosts:
        :param content_sources:
        :param current_page:
        :param facets:
        :param filters:
        :param page_size:
        :param query:
        :param result_fields:
        :param search_fields:
        :param sort:
        :param source_type:
        :param timeout:
        """
        __body: t.Dict[str, t.Any] = {}
        if automatic_query_refinement is not None:
            __body["automatic_query_refinement"] = automatic_query_refinement
        if boosts is not None:
            __body["boosts"] = boosts
        if content_sources is not None:
            __body["content_sources"] = content_sources
        if current_page is not None:
            __body.setdefault("page", {})
            __body["page"]["current"] = current_page
        if facets is not None:
            __body["facets"] = facets
        if filters is not None:
            __body["filters"] = filters
        if page_size is not None:
            __body.setdefault("page", {})
            __body["page"]["size"] = page_size
        if query is not None:
            __body["query"] = query
        if result_fields is not None:
            __body["result_fields"] = result_fields
        if search_fields is not None:
            __body["search_fields"] = search_fields
        if sort is not None:
            __body["sort"] = sort
        if source_type is not None:
            __body["source_type"] = source_type
        if timeout is not None:
            __body["timeout"] = timeout
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", "/api/ws/v1/search", body=__body, headers=__headers
        )
