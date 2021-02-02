<p align="center">
  <a href="https://github.com/elastic/enterprise-search-python">
    <img src="https://raw.githubusercontent.com/elastic/enterprise-search-python/master/assets/elastic-enterprise-search-logo.png" width="70%" alt="Elastic Enterprise Search" />
  </a>
</p>
<p align="center">
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/badge/pypi-v7.10.0b1-orange" alt="PyPI Version"></a>
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/badge/python-2.7%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue" alt="Supported Python Versions"></a>
<a href="https://pepy.tech/project/elastic-enterprise-search"><img src="https://pepy.tech/badge/elastic-enterprise-search" alt="Downloads"></a>
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/pypi/status/elastic-enterprise-search.svg" alt="Package Status"></a>
<a href="https://clients-ci.elastic.co/job/elastic+elastic-enterprise-search+master"><img src="https://clients-ci.elastic.co/buildStatus/icon?job=elastic%2Belastic-enterprise-search%2Bmaster" alt="Build Status"></a>
<a href="https://github.com/elastic/enterprise-search-python/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/elastic-enterprise-search.svg" alt="License"></a>
</p>

Official Python client for Elastic Enterprise Search, App Search, and Workplace Search

## Installation

The package can be installed from [PyPI](https://pypi.org/project/elastic-enterprise-search):

```bash
$ python -m pip install --pre elastic-enterprise-search
```

The version follows the Elastic Stack version so `7.11` is compatible
with Enterprise Search released in Elastic Stack 7.11.

> **NOTE: The package `elastic-enterprise-search` was previously used as a client for
> only 'Elastic Workplace Search' before the product was renamed. When installing
> make sure you receive a version greater than 7.10.0.**

## Documentation

Documentation on compatibility, configuring, and an API reference
is available on [elastic.co/guide](https://www.elastic.co/guide/en/enterprise-search-clients/python/current/index.html).

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
  - [Custom Source API Key](https://www.elastic.co/guide/en/workplace-search/current/workplace-search-custom-sources-api.html#authentication)
  - [OAuth for Search](https://www.elastic.co/guide/en/workplace-search/current/building-custom-search-workplace-search.html#configuring-search-oauth)

#### Authenticating with Enterprise Search

```python
from elastic_enterprise_search import EnterpriseSearch

ent = EnterpriseSearch(...)

# Authenticating via Basic Auth for Enterprise Search APIs
ent.http_auth = ("enterprise_search", "<password>")

# Authenticating with Workplace Search
# Custom API Content Source access token
ent.workplace_search.http_auth = "<content source access token>"

# You can also use an authentication method for a single
# request. This is useful for per-user authentication like OAuth:
ent.workplace_search.search(
    body={"query": "That one document"},
    http_auth="oauth-access-token"
)
```

#### App Search Signed Search Keys

```python
from elastic_enterprise_search import AppSearch

# Create an AppSearch client authenticated with a search key.
server_side = AppSearch(
    "https://<...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth="search-..."
)

# Creating a Signed Search Key on the server side...
signed_search_key = server_side.create_signed_search_key(
    api_key=server_side.http_auth,
    api_key_name="<api key name>",
    search_fields={
        "body": {}
    }   
)

# ...then a different client can then
# use the Signed Search key for searches:
client_side = AppSearch(
    "https://<...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth=signed_search_key
)
resp = client_side.search(
    engine_name="example-engine",
    body={
        ...
    }
)
```

### Working with Datetimes

Python [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)
objects are automatically serialized according to [RFC 3339](https://tools.ietf.org/html/rfc3339)
which requires a timezone to be included. We highly recommend using datetimes that
are timezone-aware. When creating a datetime object, use the `tzinfo` or `tz` parameter
along with [`python-dateutil`](https://dateutil.readthedocs.io) to ensure proper
timezones on serialized `datetime` objects.

To get the current day and time in UTC you can do the following:

```python
import datetime
from dateutil import tz

now = datetime.datetime.now(tz=tz.UTC)
```

⚠️ **Datetimes without timezone information will be serialized as if they were within
the locally configured timezone.** This is in line with HTTP and RFC 3339 specs
which state that datetimes without timezone information should be assumed to be local time.

⚠️ [**Do not use `datetime.datetime.utcnow()` or `utcfromtimestamp()`!**](https://blog.ganssle.io/articles/2019/11/utcnow.html)
These APIs don't add timezone information to the resulting datetime which causes the
serializer to return incorrect results.

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

Parameters:
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

##### [`EnterpriseSearch.get_read_only()`](https://www.elastic.co/guide/en/enterprise-search/current/read-only-api.html#getting-read-only-state)

Get the read-only flag's state

Parameters:
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

Parameters:
- `params`: Additional query params to send with the request
- `headers`: Additional headers to send with the request
- `http_auth`: Access token or HTTP basic auth username
  and password to send with the request

</details>

## Contributing

If you'd like to make a contribution to `enterprise-search-python` we 
provide [contributing documentation](https://github.com/elastic/enterprise-search-python/tree/master/CONTRIBUTING.md)
to ensure your first contribution goes smoothly.

## License

`enterprise-search-python` is available under the Apache-2.0 license.
For more details see [LICENSE](https://github.com/elastic/enterprise-search-python/blob/master/LICENSE).
