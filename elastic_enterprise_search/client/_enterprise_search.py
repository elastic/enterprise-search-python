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

from .._utils import DEFAULT, SKIP_IN_PATH, make_params, make_path  # noqa: F401
from ._base import BaseClient


class EnterpriseSearch(BaseClient):
    def get_health(
        self,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Get information on the health of a deployment and basic statistics around
        resource usage

        `<https://www.elastic.co/guide/en/enterprise-search/7.10/monitoring-apis.html#health-api-example>`_

        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        """
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "ent",
                "v1",
                "internal",
                "health",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_read_only(
        self,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Get the read-only flag's state

        `<https://www.elastic.co/guide/en/enterprise-search/7.10/read-only-api.html#getting-read-only-state>`_

        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        """
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "ent",
                "v1",
                "internal",
                "read_only_mode",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def put_read_only(
        self,
        body,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Update the read-only flag's state

        `<https://www.elastic.co/guide/en/enterprise-search/7.10/read-only-api.html#setting-read-only-state>`_

        :arg body: HTTP request body
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        """
        return self.perform_request(
            "PUT",
            make_path(
                "api",
                "ent",
                "v1",
                "internal",
                "read_only_mode",
            ),
            body=body,
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_stats(
        self,
        include=None,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Get information about the resource usage of the application, the state of
        different internal queues, etc.

        `<https://www.elastic.co/guide/en/enterprise-search/7.10/monitoring-apis.html#stats-api-example>`_

        :arg include: Comma-separated list of stats to return
        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        """
        params = make_params(
            params,
            {
                "include": include,
            },
        )
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "ent",
                "v1",
                "internal",
                "stats",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )

    def get_version(
        self,
        params=None,
        headers=None,
        http_auth=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=(),
    ):
        """
        Get version information for this server

        `<https://www.elastic.co/guide/en/enterprise-search/7.10/management-apis.html>`_

        :arg params: Additional query params to send with the request
        :arg headers: Additional headers to send with the request
        :arg http_auth: Access token or HTTP basic auth username
            and password to send with the request
        :arg request_timeout: Timeout in seconds
        :arg ignore_status: HTTP status codes to not raise an error
        :raises elastic_enterprise_search.UnauthorizedError:
        """
        return self.perform_request(
            "GET",
            make_path(
                "api",
                "ent",
                "v1",
                "internal",
                "version",
            ),
            params=params,
            headers=headers,
            http_auth=http_auth,
            request_timeout=request_timeout,
            ignore_status=ignore_status,
        )
