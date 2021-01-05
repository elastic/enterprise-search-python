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

## Installation

The package can be installed from PyPI:

```bash
$ python -m pip install elastic-enterprise-search
```

The version follows the Elastic Stack version so `7.10` is compatible
with Enterprise Search released in Elastic Stack 7.10.

> **NOTE: The package `elastic-enterprise-search` was previously used as a client for
> only 'Elastic Workplace Search' before the product was renamed. When installing
> make sure you receive a version greater than 7.10.0.**

## Getting Started

Here's how you can get started:

```python
>>> from elastic_enterprise_search import EnterpriseSearch

# Connecting to an instance on Elastic Cloud w/ username and password
>>> ent_search = EnterpriseSearch(
    "https://<...>.ent-search.us-central1.gcp.cloud.es.io",
    http_auth=("elastic", "<password>"),
)
>>> ent_search.get_version()
{'number': '7.10.0', 'build_hash': '9d6eb9f067b7d7090c541890c21f6a1e15f29c48', 'build_date': '2020-10-05T16:19:16Z'}

# If you're only planning on using App Search you
# can instantiate App Search namespaced client by itself:
>>> from elastic_enterprise_search import AppSearch

# Connecting to an instance on Elastic Cloud w/ an App Search private key
>>> app_search = AppSearch(
    "https://<...>.ent-search.us-central1.gcp.cloud.es.io",
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

## License

`enterprise-search-python` is available under the Apache-2.0 license.
For more details see [LICENSE](https://github.com/elastic/enterprise-search-python/blob/maaster/LICENSE).
