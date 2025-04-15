# :warning: App Search and Workplace Search will be discontinued in 9.0

Starting with Elastic version 9.0, the standalone Enterprise Search products, will no longer be included in our offering.
They remain supported in their current form in version 8.x and will only receive security upgrades and fixes.
Enterprise Search clients will continue to be supported in their current form throughout 8.x versions, according to our [EOL policy](https://www.elastic.co/support/eol).
We recommend transitioning to our actively developed [Elastic Stack](https://www.elastic.co/elastic-stack) tools for your search use cases. However, if you're still using any Enterprise Search products, we recommend using the latest stable release of the clients.

Here are some useful links with more information:

- [Enterprise Search FAQ](https://www.elastic.co/resources/enterprise-search/enterprise-search-faq)
- [One stop shop for Upgrading to Elastic Search 9](https://www.elastic.co/guide/en/enterprise-search/current/upgrading-to-9-x.html)

<p align="center">
  <a href="https://github.com/elastic/enterprise-search-python">
    <img src="https://raw.githubusercontent.com/elastic/enterprise-search-python/main/assets/elastic-enterprise-search-logo.png" width="70%" alt="Elastic Enterprise Search" />
  </a>
</p>
<p align="center">
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/pypi/v/elastic-enterprise-search" alt="PyPI Version"></a>
<a href="https://pypi.org/project/elastic-enterprise-search"><img src="https://img.shields.io/badge/python-2.7%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue" alt="Supported Python Versions"></a>
<a href="https://pepy.tech/project/elastic-enterprise-search"><img src="https://pepy.tech/badge/elastic-enterprise-search" alt="Downloads"></a>
<a href="https://buildkite.com/elastic/enterprise-search-python-test"><img src="https://badge.buildkite.com/52eefb5552fe436257c38234d19d9d457e5140b621ccb910e9.svg" alt="Buildkite Status"></a>
</p>


Official Python client for Elastic Enterprise Search, App Search, and Workplace Search

## Installation

The package can be installed from [PyPI](https://pypi.org/project/elastic-enterprise-search):

```bash
$ python -m pip install elastic-enterprise-search
```

The version follows the Elastic Stack version so `7.11` is compatible
with Enterprise Search released in Elastic Stack 7.11.

## Documentation

[See the documentation](https://www.elastic.co/guide/en/enterprise-search-clients/python) for how to get started,
compatibility info, configuring, and an API reference.

## Contributing

If you'd like to make a contribution to `enterprise-search-python` we 
provide [contributing documentation](https://github.com/elastic/enterprise-search-python/tree/main/CONTRIBUTING.md)
to ensure your first contribution goes smoothly.

## License

`enterprise-search-python` is available under the Apache-2.0 license.
For more details see [LICENSE](https://github.com/elastic/enterprise-search-python/blob/main/LICENSE).
