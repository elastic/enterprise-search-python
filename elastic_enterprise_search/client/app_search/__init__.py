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
    ):
        # type: (...) -> JSONResponse
        """
        The API Log displays API request and response data at the Engine level.
        
        `<https://swiftype.com/documentation/app-search/api/logs>`_
        
        :arg engine_name: Name of the engine.
        :arg from_date: Filter date from.
        :arg to_date: Filter date to.
        :arg current_page: The page to fetch. Defaults to 1.
        :arg page_size: The number of results per page.
        :arg query: Use this to specify a particular endpoint, like analytics,
            search, curations and so on.
        :arg http_status_filter: Filter based on a particular status code: 400,
            401, 403, 429, 200.
        :arg http_method_filter: Filter based on a particular HTTP method: GET,
            POST, PUT, PATCH, DELETE.
        :arg sort_direction: Would you like to have your results ascending,
            oldest to newest, or descending, newest to oldest?
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
                "filters.date.from": from_date,
                "filters.date.to": to_date,
                "page.current": current_page,
                "page.size": page_size,
                "query": query,
                "filters.status": http_status_filter,
                "filters.method": http_method_filter,
                "sort_direction": sort_direction,
            },
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines", engine_name, "logs", "api"),
                params=params,
                headers=headers,
            )
        )

    def get_count_analytics(
        self, engine_name, filters=None, interval=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Returns the number of clicks and total number of queries over a period.
        
        `<https://swiftype.com/documentation/app-search/api/analytics/counts>`_
        
        :arg engine_name: Name of the engine.
        :arg filters: Analytics filters
        :arg interval: You can define an interval along with your date range.
            Can be either hour or day.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(params, {"filters": filters, "interval": interval})
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "analytics", "counts",
                ),
                params=params,
                headers=headers,
            )
        )

    def create_curation(
        self,
        engine_name,
        queries,
        promoted_doc_ids=None,
        hidden_doc_ids=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Create a new curation.
        
        `<https://swiftype.com/documentation/app-search/api/curations#create>`_
        
        :arg engine_name: Name of the engine.
        :arg queries: List of affected search queries.
        :arg promoted_doc_ids: List of promoted document ids.
        :arg hidden_doc_ids: List of hidden document ids.
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
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "curations"),
                params=params,
                headers=headers,
            )
        )

    def delete_curation(
        self, engine_name, curation_id, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Delete a curation by id.
        
        `<https://swiftype.com/documentation/app-search/api/curations#destroy>`_
        
        :arg engine_name: Name of the engine.
        :arg curation_id: Curation id.
        """

        for param in (
            engine_name,
            curation_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "DELETE",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "curations", curation_id,
                ),
                params=params,
                headers=headers,
            )
        )

    def get_curation(
        self, engine_name, curation_id, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieve a curation by id.
        
        `<https://swiftype.com/documentation/app-search/api/curations#single>`_
        
        :arg engine_name: Name of the engine.
        :arg curation_id: Curation id.
        """

        for param in (
            engine_name,
            curation_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "curations", curation_id,
                ),
                params=params,
                headers=headers,
            )
        )

    def update_curation(
        self,
        engine_name,
        curation_id,
        queries,
        promoted_doc_ids=None,
        hidden_doc_ids=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Update an existing curation.
        
        `<https://swiftype.com/documentation/app-search/api/curations#update>`_
        
        :arg engine_name: Name of the engine.
        :arg curation_id: Curation id.
        :arg queries: List of affected search queries.
        :arg promoted_doc_ids: List of promoted document ids.
        :arg hidden_doc_ids: List of hidden document ids.
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
        return JSONResponse(
            *self.transport.request(
                "PUT",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "curations", curation_id,
                ),
                params=params,
                headers=headers,
            )
        )

    def list_curations(
        self, engine_name, current_page=None, page_size=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieve available curations for the engine.
        
        `<https://swiftype.com/documentation/app-search/api/curations#read>`_
        
        :arg engine_name: Name of the engine.
        :arg current_page: The page to fetch. Defaults to 1.
        :arg page_size: The number of results per page.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"page.current": current_page, "page.size": page_size}
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines", engine_name, "curations"),
                params=params,
                headers=headers,
            )
        )

    def delete_documents(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Delete documents by id.
        
        `<https://swiftype.com/documentation/app-search/api/documents#partial>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "DELETE",
                make_path("api", "as", "v1", "engines", engine_name, "documents"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def get_documents(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieves one or more documents by id.
        
        `<https://swiftype.com/documentation/app-search/api/documents#get>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines", engine_name, "documents"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def list_documents(
        self, engine_name, current_page=None, page_size=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        List all available documents with optional pagination support.
        
        `<https://swiftype.com/documentation/app-search/api/documents#list>`_
        
        :arg engine_name: Name of the engine.
        :arg current_page: The page to fetch. Defaults to 1.
        :arg page_size: The number of results per page.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"page.current": current_page, "page.size": page_size}
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "documents", "list",
                ),
                params=params,
                headers=headers,
            )
        )

    def update_documents(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Partial update of documents.
        
        `<https://swiftype.com/documentation/app-search/api/documents#partial>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "PATCH",
                make_path("api", "as", "v1", "engines", engine_name, "documents"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def create_engine(
        self,
        name,
        language=None,
        type=None,
        source_engines=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Creates a new engine.
        
        `<https://swiftype.com/documentation/app-search/api/engines#create>`_
        
        :arg name: Engine name.
        :arg language: Engine language (null for universal).
        :arg type: Engine type.
        :arg source_engines: Sources engines list.
        """

        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params,
            {
                "name": name,
                "language": language,
                "type": type,
                "source_engines": source_engines,
            },
        )
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines"),
                params=params,
                headers=headers,
            )
        )

    def delete_engine(
        self, engine_name, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Delete an engine by name.
        
        `<https://swiftype.com/documentation/app-search/api/engines#delete>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "DELETE",
                make_path("api", "as", "v1", "engines", engine_name),
                params=params,
                headers=headers,
            )
        )

    def get_engine(
        self, engine_name, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieves an engine by name.
        
        `<https://swiftype.com/documentation/app-search/api/engines#get>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines", engine_name),
                params=params,
                headers=headers,
            )
        )

    def list_engines(
        self, current_page=None, page_size=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieves all engines with optional pagination support.
        
        `<https://swiftype.com/documentation/app-search/api/engines#list>`_
        
        :arg current_page: The page to fetch. Defaults to 1.
        :arg page_size: The number of results per page.
        """

        params = make_params(
            params, {"page.current": current_page, "page.size": page_size}
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines"),
                params=params,
                headers=headers,
            )
        )

    def index_documents(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Create or update documents.
        
        `<https://swiftype.com/documentation/app-search/api/documents#create>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "documents"),
                body=body,
                params=params,
                headers=headers,
            )
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
    ):
        # type: (...) -> JSONResponse
        """
        Send data about clicked results.
        
        `<https://swiftype.com/documentation/app-search/api/clickthrough>`_
        
        :arg engine_name: Name of the engine.
        :arg query_text: Search query text.
        :arg document_id: The id of the document that was clicked on.
        :arg request_id: The request id returned in the meta tag of a search API
            response.
        :arg tags: Array of strings representing additional information you wish
            to track with the clickthrough.
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
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "click"),
                params=params,
                headers=headers,
            )
        )

    def add_meta_engine_source(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Add a source engine to an existing meta engine.
        
        `<https://swiftype.com/documentation/app-search/api/meta-engines#add-source-engines>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "source_engines"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def delete_meta_engine_source(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Delete a source engine from a meta engine.
        
        `<https://swiftype.com/documentation/app-search/api/meta-engines#remove-source-engines>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "DELETE",
                make_path("api", "as", "v1", "engines", engine_name, "source_engines"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def multi_search(
        self, engine_name, queries, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Run several search in the same request.
        
        `<https://swiftype.com/documentation/app-search/api/search#multi>`_
        
        :arg engine_name: Name of the engine.
        :arg queries: Search queries.
        """

        for param in (
            engine_name,
            queries,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(params, {"queries": queries})
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "multi_search"),
                params=params,
                headers=headers,
            )
        )

    def query_suggestion(
        self, engine_name, query, fields=None, size=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Provide relevant query suggestions for incomplete queries.
        
        `<https://swiftype.com/documentation/app-search/api/query-suggestion>`_
        
        :arg engine_name: Name of the engine.
        :arg query: A partial query for which to receive suggestions.
        :arg fields: List of fields to use to generate suggestions. Defaults to
            all text fields.
        :arg size: Number of query suggestions to return. Must be between 1 and
            20. Defaults to 5.
        """

        for param in (
            engine_name,
            query,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"query": query, "types.documents.fields": fields, "size": size}
        )
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "query_suggestion",
                ),
                params=params,
                headers=headers,
            )
        )

    def reset_search_settings(
        self, engine_name, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Reset search settings for the engine.
        
        `<https://swiftype.com/documentation/app-search/api/search-settings#reset>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def get_schema(
        self, engine_name, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieve current schema for then engine.
        
        `<https://swiftype.com/documentation/app-search/api/schema#read>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines", engine_name, "schema"),
                params=params,
                headers=headers,
            )
        )

    def update_schema(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Update schema for the current engine.
        
        `<https://swiftype.com/documentation/app-search/api/schema#patch>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "schema"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def search(
        self, engine_name, query_text, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Allows you to search over, facet and filter your data.
        
        `<https://swiftype.com/documentation/app-search/api/search>`_
        
        :arg engine_name: Name of the engine.
        :arg query_text: Search query text.
        """

        for param in (
            engine_name,
            query_text,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(params, {"query": query_text})
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "search"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def get_search_settings(
        self, engine_name, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrive current search settings for the engine.
        
        `<https://swiftype.com/documentation/app-search/api/search-settings#show>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "search_settings",
                ),
                params=params,
                headers=headers,
            )
        )

    def update_search_settings(
        self, engine_name, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Update search settings for the engine.
        
        `<https://swiftype.com/documentation/app-search/api/search-settings#update>`_
        
        :arg engine_name: Name of the engine.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
                "PUT",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "search_settings",
                ),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def create_synonym_set(
        self, engine_name, synonyms, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Create a new synonym set.
        
        `<https://swiftype.com/documentation/app-search/api/synonyms#create>`_
        
        :arg engine_name: Name of the engine.
        :arg synonyms: List of synonyms words.
        """

        for param in (
            engine_name,
            synonyms,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        params = make_params(params, {"synonyms": synonyms})
        return JSONResponse(
            *self.transport.request(
                "POST",
                make_path("api", "as", "v1", "engines", engine_name, "synonyms"),
                params=params,
                headers=headers,
            )
        )

    def delete_synonym_set(
        self, engine_name, synonym_set_id, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Delete a synonym set by id.
        
        `<https://swiftype.com/documentation/app-search/api/synonyms#delete>`_
        
        :arg engine_name: Name of the engine.
        :arg synonym_set_id: Synonym set id.
        """

        for param in (
            engine_name,
            synonym_set_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def get_synonym_set(
        self, engine_name, synonym_set_id, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieve a synonym set by id.
        
        `<https://swiftype.com/documentation/app-search/api/synonyms#list-one>`_
        
        :arg engine_name: Name of the engine.
        :arg synonym_set_id: Synonym set id.
        """

        for param in (
            engine_name,
            synonym_set_id,
        ):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument")

        return JSONResponse(
            *self.transport.request(
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
            )
        )

    def list_synonym_sets(
        self, engine_name, current_page=None, page_size=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Retrieve available synonym sets for the engine.
        
        `<https://swiftype.com/documentation/app-search/api/synonyms#get>`_
        
        :arg engine_name: Name of the engine.
        :arg current_page: The page to fetch. Defaults to 1.
        :arg page_size: The number of results per page.
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"page.current": current_page, "page.size": page_size}
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "as", "v1", "engines", engine_name, "synonyms"),
                params=params,
                headers=headers,
            )
        )

    def get_top_clicks_analytics(
        self,
        engine_name,
        query=None,
        page_size=None,
        filters=None,
        params=None,
        headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Returns the number of clicks received by a document in descending order.
        
        `<https://swiftype.com/documentation/app-search/api/analytics/clicks>`_
        
        :arg engine_name: Name of the engine.
        :arg query: Filter clicks over a search query.
        :arg page_size: The number of results per page.
        :arg filters: Analytics filters
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(
            params, {"query": query, "page.size": page_size, "filters": filters}
        )
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "analytics", "clicks",
                ),
                params=params,
                headers=headers,
            )
        )

    def get_top_queries_analytics(
        self, engine_name, page_size=None, filters=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Returns queries anlaytics by usage count.
        
        `<https://swiftype.com/documentation/app-search/api/analytics/queries>`_
        
        :arg engine_name: Name of the engine.
        :arg page_size: The number of results per page.
        :arg filters: Analytics filters
        """

        if engine_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument")

        params = make_params(params, {"page.size": page_size, "filters": filters})
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path(
                    "api", "as", "v1", "engines", engine_name, "analytics", "queries",
                ),
                params=params,
                headers=headers,
            )
        )
