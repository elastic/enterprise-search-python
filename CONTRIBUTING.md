# Contributing to enterprise-search-python

## Contributing Code Changes

1. Please make sure you have signed the [Contributor License
   Agreement](http://www.elastic.co/contributor-agreement/). We are not
   asking you to assign copyright to us, but to give us the right to distribute
   your code without restriction. We ask this of all contributors in order to
   assure our users of the origin and continuing existence of the code. You only
   need to sign the CLA once.
 
2. Run the linter and test suite to ensure your changes do not break existing code:

   Install [`nox`](https://nox.thea.codes) for task management:

   ```
   $ python -m pip install nox
   ```

   Auto-format and lint your changes:

   ```
   $ nox -rs format
   ```
   
   Run the test suite:

   ```
   # Runs against Python 2.7 and 3.6
   $ nox -rs test-2.7 test-3.6
   
   # Runs against all available Python versions
   $ nox -rs test
   ```

3. Rebase your changes. Update your local repository with the most recent code
   from the main `enterprise-search-python` repository and rebase your branch
   on top of the latest `main` branch. All of your changes will be squashed
   into a single commit so don't worry about pushing multiple times.
   
4. Submit a pull request. Push your local changes to your forked repository
   and [submit a pull request](https://github.com/elastic/enterprise-search-python/pulls)
   and mention the issue number if any (`Closes #123`) Make sure that you
   add or modify tests related to your changes so that CI will pass.
   
5. Sit back and wait. There may be some discussion on your pull request and
   if changes are needed we would love to work with you to get your pull request
   merged into enterprise-search-python.

## Running Integration Tests

Run the full integration test suite with `$ .ci/run-tests`.

There are several environment variabels that control integration tests:

- `PYTHON_VERSION`: Version of Python to use, defaults to `3.9`
- `STACK_VERSION`: Version of Elasticsearch to use. These should be
  the same as tags of `docker.elastic.co/elasticsearch/elasticsearch`
  such as `8.0.0-SNAPSHOT`, `7.11-SNAPSHOT`, etc. Defaults to the
  same `*-SNAPSHOT` version as the branch.
- `ENTERPRISE_SEARCH_URL`: URL for the Enterprise Search instance
- `ENTERPRISE_SEARCH_PASSWORD`: Password for the `elastic` user on Enterprise Search. This is typically the same as the `elastic` password on Elasticsearch.
- `APP_SEARCH_PRIVATE_KEY`: Private key for App Search
