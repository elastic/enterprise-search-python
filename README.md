# Python Enterprise Search Client

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
from elastic_enterprise_search import EnterpriseSearch

ent = EnterpriseSearch(
    # Connecting to an instance on Elastic Cloud
    host="https://<a9ddd...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth=("elastic", "<password>"),
    use_ssl=True,
)
print(ent.get_version())

# If you're only planning on using App Search you
# can instantiate App Search namespaced client by itself:

from elastic_enterprise_search import AppSearch

app_search = AppSearch(
    # Connecting to an instance on Elastic Cloud
    host="https://<a9ddd...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth=("elastic", "<password>"),
    use_ssl=True
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
- [App Search](https://swiftype.com/documentation/app-search/authentication)
  - [Public Search Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-search)
  - [Private API Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-private)
  - [Private Admin Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-admin)
  - [Signed Search Key](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-signed)
  - [URL Parameters](https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-url-params)
- Workplace Search
  - [Custom Source API Key](https://www.elastic.co/guide/en/workplace-search/7.8/workplace-search-custom-sources-api.html#authentication)

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
```

## License

Apache-2.0
