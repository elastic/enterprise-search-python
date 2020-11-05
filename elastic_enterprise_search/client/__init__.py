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

import jwt
from six import ensure_str

from .._utils import DEFAULT
from ._app_search import AppSearch as _AppSearch
from ._enterprise_search import EnterpriseSearch as _EnterpriseSearch
from ._workplace_search import WorkplaceSearch as _WorkplaceSearch

__all__ = ["AppSearch", "EnterpriseSearch", "WorkplaceSearch"]


class AppSearch(_AppSearch):
    """Client for Elastic App Search service

    `<https://www.elastic.co/guide/en/app-search/current/api-reference.html>`_
    """

    @staticmethod
    def create_signed_search_key(
        api_key,
        api_key_name,
        search_fields=DEFAULT,
        result_fields=DEFAULT,
        filters=DEFAULT,
        facets=DEFAULT,
    ):
        """Creates a Signed Search Key to keep your Private API Key secret
        and restrict what a user can search over.

        `<https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-signed>`_

        :arg api_key: API key to use for signing
        :arg api_key_name: Name of the API key used for signing
        :arg search_fields: Fields to search over.
        :arg result_fields: Fields to return in the result
        :arg filters: Adds filters to the search requests
        :arg facets: Sets the facets that are allowed.
            To disable aggregations set to '{}' or 'None'.
        """
        options = {
            k: v
            for k, v in (
                ("api_key_name", api_key_name),
                ("search_fields", search_fields),
                ("result_fields", result_fields),
                ("filters", filters),
                ("facets", facets),
            )
            if v is not DEFAULT
        }
        return ensure_str(jwt.encode(payload=options, key=api_key, algorithm="HS256"))


class WorkplaceSearch(_WorkplaceSearch):
    """Client for Workplace Search

    `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-api-overview.html>`_
    """


class EnterpriseSearch(_EnterpriseSearch):
    """Client for Enterprise Search

    `<https://www.elastic.co/guide/en/enterprise-search/current/management-apis.html>`_
    """

    def __init__(self, hosts=None, transport_class=None, **kwargs):
        """
        :arg hosts: List of nodes, or a single node, we should connect to.
            Node should be a dictionary ({"host": "localhost", "port": 3002}),
            the entire dictionary will be passed to the :class:`~elastic_transport.Connection`
            class as kwargs, or a string in the format of ``host[:port]`` which will be
            translated to a dictionary automatically.  If no value is given the
            :class:`~elastic_transport.Connection` class defaults will be used.

        :arg transport_class: :class:`~elastic_transport.Transport` sub-class to use.

        :arg kwargs: Any additional arguments will be passed on to the
            :class:`~elastic_transport.Transport` class and, subsequently, to the
            :class:`~elastic_transport.Connection` instances.
        """
        super(EnterpriseSearch, self).__init__(
            hosts=hosts, transport_class=transport_class, **kwargs
        )

        self.app_search = AppSearch(_transport=self.transport)
        self.workplace_search = WorkplaceSearch(_transport=self.transport)
