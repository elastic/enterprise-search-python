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

from ..._utils import _quote_query_form, _rewrite_parameters
from ._base import BaseClient


class AsyncEnterpriseSearch(BaseClient):
    # AUTO-GENERATED-API-DEFINITIONS #

    @_rewrite_parameters()
    async def get_health(
        self,
    ) -> t.Any:
        """
        Get information on the health of a deployment and basic statistics around resource
        usage

        `<https://www.elastic.co/guide/en/enterprise-search/current/monitoring-apis.html#health-api-example>`_
        """
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ent/v1/internal/health", headers=__headers
        )

    @_rewrite_parameters()
    async def get_read_only(
        self,
    ) -> t.Any:
        """
        Get the read-only flag's state

        `<https://www.elastic.co/guide/en/enterprise-search/current/read-only-api.html#getting-read-only-state>`_
        """
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ent/v1/internal/read_only_mode", headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    async def put_read_only(
        self,
        *,
        enabled: bool,
    ) -> t.Any:
        """
        Update the read-only flag's state

        `<https://www.elastic.co/guide/en/enterprise-search/current/read-only-api.html#setting-read-only-state>`_

        :param enabled:
        """
        if enabled is None:
            raise ValueError("Empty value passed for parameter 'enabled'")
        __body: t.Dict[str, t.Any] = {}
        if enabled is not None:
            __body["enabled"] = enabled
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "PUT", "/api/ent/v1/internal/read_only_mode", body=__body, headers=__headers
        )

    @_rewrite_parameters()
    async def get_stats(
        self,
        *,
        include: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> t.Any:
        """
        Get information about the resource usage of the application, the state of different
        internal queues, etc.

        `<https://www.elastic.co/guide/en/enterprise-search/current/monitoring-apis.html#stats-api-example>`_

        :param include: Comma-separated list of stats to return
        """
        __query: t.Dict[str, t.Any] = {}
        if include is not None:
            __query["include"] = _quote_query_form("include", include)
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ent/v1/internal/stats", params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_version(
        self,
    ) -> t.Any:
        """
        Get version information for this server

        `<https://www.elastic.co/guide/en/enterprise-search/current/management-apis.html>`_
        """
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", "/api/ent/v1/internal/version", headers=__headers
        )
