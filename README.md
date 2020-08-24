<p align="center">
  <a href="https://github.com/elastic/enterprise-search-python">
    <img src="https://raw.githubusercontent.com/elastic/enterprise-search-python/master/assets/elastic-enterprise-search-logo.png" width="70%" alt="Elastic Enterprise Search" />
  </a>
</p>
<p align="center">
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/pypi/v/elastic-enterprise-search.svg" alt="PyPI Version"></a>
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/pypi/pyversions/elastic-enterprise-search" alt="Supported Python Versions"></a>
<a href="https://pepy.tech/project/elastic-enterprise-search"><img src="https://pepy.tech/badge/elastic-enterprise-search" alt="Downloads"></a>
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/pypi/status/elastic-enterprise-search.svg" alt="Package Status"></a>
<a href="https://clients-ci.elastic.co/job/elastic+elastic-enterprise-search+master"><img src="https://clients-ci.elastic.co/buildStatus/icon?job=elastic%2Belastic-enterprise-search%2Bmaster" alt="Build Status"></a>
<a href="https://github.com/elastic/enterprise-search-python/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/elastic-enterprise-search.svg" alt="License"></a>
</p>

## Table of Contents

- [Installation](https://github.com/elastic/enterprise-search-python#installation)
- [Getting Started](https://github.com/elastic/enterprise-search-python#getting-started)
  - [Authentication](https://github.com/elastic/enterprise-search-python#authentication)
- [API Reference](https://github.com/elastic/enterprise-search-python#api-reference)
- [License](https://github.com/elastic/enterprise-search-python#license)

## Installation

The package can be installed from PyPI:

```bash
$ python -m pip install elastic-enterprise-search
```

The version follows the Elastic Stack version so `7.10` is compatible
with Enterprise Search released in Elastic Stack 7.10.

## Getting Started

Here's how you can get started:

```python
>>> from elastic_enterprise_search import EnterpriseSearch

# Connecting to an instance on Elastic Cloud w/ username and password
>>> ent = EnterpriseSearch(
    host="https://<...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth=("elastic", "<password>"),
)
>>> ent.get_version()
{'number': '7.8.1', 'build_hash': '0b11f494eadfe43dbb141cf80fb0848019593edc', 'build_date': '2020-07-21T19:13:24Z'}

# If you're only planning on using App Search you
# can instantiate App Search namespaced client by itself:
>>> from elastic_enterprise_search import AppSearch

# Connecting to an instance on Elastic Cloud w/ an App Search private key
>>> app_search = AppSearch(
    host="https://<...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth="private-<private key>",
)
>>> app_search.index_documents(
    engine_name="national-parks",
    body=[{
        "id": "yellowstone",
        "title": "Yellowstone National Park"
    }]
)
```

### Authentication

Each service has its own authentication schemes.
Using the `http_auth` property with either a string
for a key / token or a tuple of `(username, password)`
for basic authentication will set the proper
`Authorization` HTTP header on the client instance.

- Enterprise Search
  - Basic Authentication (Username / Password)
- [App Search](https://www.elastic.co/guide/en/app-search/current/authentication.html)
  - [Public Search Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-search)
  - [Private API Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-private)
  - [Private Admin Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-admin)
  - [Signed Search Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-signed)
  - [URL Parameters](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-url-params)
- Workplace Search
  - [Custom Source API Key](https://www.elastic.co/guide/en/workplace-search/7.8/workplace-search-custom-sources-api.html#authentication)
  - [OAuth for Search](https://www.elastic.co/guide/en/workplace-search/current/building-custom-search-workplace-search.html#configuring-search-oauth)

```python
from elastic_enterprise_search import EnterpriseSearch

ent = EnterpriseSearch(...)

# Authenticating via Basic Auth for Enterprise Search APIs
ent.http_auth = ("enterprise_search", "<password>")

# Authenticating with Workplace Search
# Custom API Content Source access token
ent.workplace_search.http_auth = "<content source access token>"

# Authenticating with App Search
ent.app_search.http_auth = "<any App Search auth key>"

# Creating a Signed Search Key with App Search
signed_key = ent.app_search.create_signed_search_key(
    api_key="<private api key>",
    api_key_name="<api key name>",
    search_fields={
        "body": {}
    }   
)
ent.app_search.http_auth = signed_key

# You can also use an authentication method for a single
# request. This is useful for per-user authentication like OAuth:
ent.workplace_search.search(
    body={"query": "That one document"},
    http_auth="oauth-access-token"
)
```

## API Reference

A list of APIs for each client along with parameters:

### App Search API

<details>
  <summary>Expand for all APIs</summary>

##### [`AppSearch.get_api_logs()`](https://www.elastic.co/guide/en/app-search/current/api-logs.html)

The API Log displays API request and response data at the Engine level

Parameters:
- `engine_name`: Name of the engine
- `from_date`: Filter date from
- `to_date`: Filter date to
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `query`: Use this to specify a particular endpoint, like analytics,
  search, curations and so on
- `http_status_filter`: Filter based on a particular status code: 400,
  401, 403, 429, 200
- `http_method_filter`: Filter based on a particular HTTP method: GET,
  POST, PUT, PATCH, DELETE
- `sort_direction`: Would you like to have your results ascending,
  oldest to newest, or descending, newest to oldest?
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_count_analytics()`](https://www.elastic.co/guide/en/app-search/current/counts.html)

Returns the number of clicks and total number of queries over a period

Parameters:
- `engine_name`: Name of the engine
- `filters`: Analytics filters
- `interval`: You can define an interval along with your date range. Can
  be either hour or day
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.create_curation()`](https://www.elastic.co/guide/en/app-search/current/curations.html#curations-create)

Create a new curation

Parameters:
- `engine_name`: Name of the engine
- `queries`: List of affected search queries
- `promoted_doc_ids`: List of promoted document IDs
- `hidden_doc_ids`: List of hidden document IDs
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.delete_curation()`](https://www.elastic.co/guide/en/app-search/current/curations.html#curations-destroy)

Delete a curation by ID

Parameters:
- `engine_name`: Name of the engine
- `curation_id`: Curation ID
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_curation()`](https://www.elastic.co/guide/en/app-search/current/curations.html#curations-read)

Retrieve a curation by ID

Parameters:
- `engine_name`: Name of the engine
- `curation_id`: Curation ID
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.put_curation()`](https://www.elastic.co/guide/en/app-search/current/curations.html#curations-update)

Update an existing curation

Parameters:
- `engine_name`: Name of the engine
- `curation_id`: Curation ID
- `queries`: List of affected search queries
- `promoted_doc_ids`: List of promoted document IDs
- `hidden_doc_ids`: List of hidden document IDs
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.list_curations()`](https://www.elastic.co/guide/en/app-search/current/curations.html#curations-read)

Retrieve available curations for the engine

Parameters:
- `engine_name`: Name of the engine
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.delete_documents()`](https://www.elastic.co/guide/en/app-search/current/documents.html#documents-delete)

Delete documents by ID

Parameters:
- `engine_name`: Name of the engine
- `body`: List of document IDs
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_documents()`](https://www.elastic.co/guide/en/app-search/current/documents.html#documents-get)

Retrieves one or more documents by ID

Parameters:
- `engine_name`: Name of the engine
- `body`: List of document IDs
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.index_documents()`](https://www.elastic.co/guide/en/app-search/current/documents.html#documents-create)

Create or update documents

Parameters:
- `engine_name`: Name of the engine
- `body`: List of document to index
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.list_documents()`](https://www.elastic.co/guide/en/app-search/current/documents.html#documents-list)

List all available documents with optional pagination support

Parameters:
- `engine_name`: Name of the engine
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.put_documents()`](https://www.elastic.co/guide/en/app-search/current/documents.html#documents-partial)

Partial update of documents

Parameters:
- `engine_name`: Name of the engine
- `body`: List of documents to update
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.create_engine()`](https://www.elastic.co/guide/en/app-search/current/engines.html#engines-create)

Creates a new engine

Parameters:
- `engine_name`: Engine name
- `language`: Engine language (null for universal)
- `type`: Engine type
- `source_engines`: Sources engines list
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.delete_engine()`](https://www.elastic.co/guide/en/app-search/current/engines.html#engines-delete)

Delete an engine by name

Parameters:
- `engine_name`: Name of the engine
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_engine()`](https://www.elastic.co/guide/en/app-search/current/engines.html#engines-get)

Retrieves an engine by name

Parameters:
- `engine_name`: Name of the engine
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.list_engines()`](https://www.elastic.co/guide/en/app-search/current/engines.html#engines-list)

Retrieves all engines with optional pagination support

Parameters:
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.log_clickthrough()`](https://www.elastic.co/guide/en/app-search/current/clickthrough.html)

Send data about clicked results

Parameters:
- `engine_name`: Name of the engine
- `query_text`: Search query text
- `document_id`: The ID of the document that was clicked on
- `request_id`: The request ID returned in the meta tag of a search API
  response
- `tags`: Array of strings representing additional information you wish
  to track with the clickthrough
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.add_meta_engine_source()`](https://www.elastic.co/guide/en/app-search/current/meta-engines.html#meta-engines-add-source-engines)

Add a source engine to an existing meta engine

Parameters:
- `engine_name`: Name of the engine
- `body`: List of engine IDs
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.delete_meta_engine_source()`](https://www.elastic.co/guide/en/app-search/current/meta-engines.html#meta-engines-remove-source-engines)

Delete a source engine from a meta engine

Parameters:
- `engine_name`: Name of the engine
- `body`: List of engine IDs
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.multi_search()`](https://www.elastic.co/guide/en/app-search/current/search.html#search-multi)

Run several search in the same request

Parameters:
- `engine_name`: Name of the engine
- `queries`: Search queries
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.query_suggestion()`](https://www.elastic.co/guide/en/app-search/current/query-suggestion.html)

Provide relevant query suggestions for incomplete queries

Parameters:
- `engine_name`: Name of the engine
- `query`: A partial query for which to receive suggestions
- `fields`: List of fields to use to generate suggestions. Defaults to
  all text fields
- `size`: Number of query suggestions to return. Must be between 1 and
  20. Defaults to 5
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_schema()`](https://www.elastic.co/guide/en/app-search/current/schema.html#schema-read)

Retrieve current schema for then engine

Parameters:
- `engine_name`: Name of the engine
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.put_schema()`](https://www.elastic.co/guide/en/app-search/current/schema.html#schema-patch)

Update schema for the current engine

Parameters:
- `engine_name`: Name of the engine
- `body`: Schema description
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.search()`](https://www.elastic.co/guide/en/app-search/current/search.html#search-single)

Allows you to search over, facet and filter your data

Parameters:
- `engine_name`: Name of the engine
- `body`: Search request parameters
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_search_settings()`](https://www.elastic.co/guide/en/app-search/current/search-settings.html#search-settings-show)

Retrive current search settings for the engine

Parameters:
- `engine_name`: Name of the engine
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.put_search_settings()`](https://www.elastic.co/guide/en/app-search/current/search-settings.html#search-settings-update)

Update search settings for the engine

Parameters:
- `engine_name`: Name of the engine
- `body`: Search settings
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.reset_search_settings()`](https://www.elastic.co/guide/en/app-search/current/search-settings.html#search-settings-reset)

Reset search settings for the engine

Parameters:
- `engine_name`: Name of the engine
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.create_synonym_set()`](https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-create)

Create a new synonym set

Parameters:
- `engine_name`: Name of the engine
- `synonyms`: List of synonyms words
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.delete_synonym_set()`](https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-delete)

Delete a synonym set by ID

Parameters:
- `engine_name`: Name of the engine
- `synonym_set_id`: Synonym set ID
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_synonym_set()`](https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-list-one)

Retrieve a synonym set by ID

Parameters:
- `engine_name`: Name of the engine
- `synonym_set_id`: Synonym set ID
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.put_synonym_set()`](https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-update)

Update a synonym set by ID

Parameters:
- `engine_name`: Name of the engine
- `synonym_set_id`: Synonym set ID
- `synonyms`: List of synonyms words
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.list_synonym_sets()`](https://www.elastic.co/guide/en/app-search/current/synonyms.html#synonyms-get)

Retrieve available synonym sets for the engine

Parameters:
- `engine_name`: Name of the engine
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_top_clicks_analytics()`](https://www.elastic.co/guide/en/app-search/current/clicks.html)

Returns the number of clicks received by a document in descending order

Parameters:
- `engine_name`: Name of the engine
- `query`: Filter clicks over a search query
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `filters`: Analytics filters
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`AppSearch.get_top_queries_analytics()`](https://www.elastic.co/guide/en/app-search/current/queries.html#queries-top-queries)

Returns queries analytics by usage count

Parameters:
- `engine_name`: Name of the engine
- `current_page`: The page to fetch. Defaults to 1
- `page_size`: The number of results per page
- `filters`: Analytics filters
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

</details>

### Workplace Search API

<details>
  <summary>Expand for all APIs</summary>

##### [`WorkplaceSearch.delete_documents()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#destroy)

Deletes a list of documents from a custom content source

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.index_documents()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#index-and-update)

Indexes one or more new documents into a custom content source, or updates one
or more existing documents

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.list_external_identities()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#list-external-identities)

Retrieves all external identities

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `current_page`: Which page of results to request
- `page_size`: The number of results to return in a page
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.create_external_identity()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#add-external-identity)

Adds a new external identity

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.delete_external_identity()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#remove-external-identity)

Deletes an external identity

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.get_external_identity()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#show-external-identity)

Retrieves an external identity

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.put_external_identity()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-external-identities-api.html#update-external-identity)

Updates an external identity

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.list_permissions()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#list)

Lists all permissions for all users

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `current_page`: Which page of results to request
- `page_size`: The number of results to return in a page
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.remove_user_permissions()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#remove-one)

Removes one or more permissions from an existing set of permissions

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.search()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-search-api.html)

search across available sources with various query tuning options

Parameters:
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.add_user_permissions()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#add-one)

Adds one or more new permissions atop existing permissions

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.get_user_permissions()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#list-one)

Lists all permissions for one user

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`WorkplaceSearch.put_user_permissions()`](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-document-permissions-api.html#add-all)

Creates a new set of permissions or over-writes all existing permissions

Parameters:
- `content_source_key`: Unique key for a Custom API source, provided
  upon creation of a Custom API Source
- `user`: The username in context
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

</details>

### Enterprise Search API

<details>
  <summary>Expand for all APIs</summary>

##### [`EnterpriseSearch.get_health()`](https://www.elastic.co/guide/en/enterprise-search/current/monitoring-apis.html#health-api-example)

Get information on the health of a deployment and basic statistics around
resource usage


- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`EnterpriseSearch.get_read_only()`](https://www.elastic.co/guide/en/enterprise-search/current/read-only-api.html#getting-read-only-state)

Get the read-only flag's state


- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`EnterpriseSearch.put_read_only()`](https://www.elastic.co/guide/en/enterprise-search/current/read-only-api.html#setting-read-only-state)

Update the read-only flag's state

Parameters:
- `body`: HTTP request body
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`EnterpriseSearch.get_stats()`](https://www.elastic.co/guide/en/enterprise-search/current/monitoring-apis.html#stats-api-example)

Get information about the resource usage of the application, the state of
different internal queues, etc.

Parameters:
- `include`: Comma-separated list of stats to return
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`EnterpriseSearch.get_version()`](https://www.elastic.co/guide/en/enterprise-search/current/management-apis.html)

Get version information for this server


- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

</details>

## License

Apache-2.0
