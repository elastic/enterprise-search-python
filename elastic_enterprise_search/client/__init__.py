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
from elastic_transport import QueryParams
from six import ensure_str
from six.moves.urllib_parse import urlencode

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

    def oauth_authorize_url(self, response_type, client_id, redirect_uri):
        """Constructs an OAuth authorize URL to start either the Confidential flow
        (response_type='code') or Implicit flow (response_type='token')

        :param response_type: Either 'code' for the confidential flow or 'token'
            for the implicit flow.
        :param client_id: Client ID as generated when setting up an OAuth application
        :param redirect_uri: Location to redirect user once the OAuth process is completed.
            Must match one of the URIs configured in the OAuth application
        :returns: URL to redirect the user to visit in a browser
        """
        if response_type not in ("token", "code"):
            raise ValueError(
                "'response_type' must be either 'code' for confidential flow"
                "or 'token' for implicit flow"
            )
        if not all(
            isinstance(param, str) for param in (response_type, client_id, redirect_uri)
        ):
            raise TypeError("All parameters must be of type 'str'")

        base_url = self.transport.get_connection().base_url.rstrip("/")
        query = urlencode(
            [
                ("response_type", response_type),
                ("client_id", client_id),
                ("redirect_uri", redirect_uri),
            ]
        )
        return "%s/ws/oauth/authorize?%s" % (base_url, query)

    def oauth_exchange_for_access_token(
        self, client_id, client_secret, redirect_uri, code=None, refresh_token=None
    ):
        """Exchanges either an authorization code or refresh token for
        an access token via the confidential OAuth flow.

        :param client_id: Client ID as generated when setting up an OAuth application
        :param client_secret: Client secret as generated when setting up an OAuth application
        :param redirect_uri: Location to redirect user once the OAuth process is completed.
            Must match one of the URIs configured in the OAuth application
        :param code: Authorization code as returned by the '/ws/oauth/authorize' endpoint
        :param refresh_token: Refresh token returned at the same time as receiving an access token
        :returns: The HTTP response containing the access_token and refresh_token
            along with other token-related metadata
        """
        values = [client_id, client_secret, redirect_uri]

        # Check that 'code' and 'refresh_token' are mutually exclusive
        if code is None and refresh_token is None:
            raise ValueError(
                "Either the 'code' or 'refresh_token' parameter must be used"
            )
        elif code is not None and refresh_token is not None:
            raise ValueError(
                "'code' and 'refresh_token' parameters are mutually exclusive"
            )
        elif code is not None:
            values.append(code)
            grant_type = "authorization_code"
        else:
            assert refresh_token is not None
            values.append(refresh_token)
            grant_type = "refresh_token"

        if not all(isinstance(value, str) for value in values):
            raise TypeError("All parameters must be of type 'str'")

        params = QueryParams()
        params.add("grant_type", grant_type)
        params.add("client_id", client_id)
        params.add("client_secret", client_secret)
        params.add("redirect_uri", redirect_uri)
        if code is not None:
            params.add("code", code)
        else:
            params.add("refresh_token", refresh_token)

        return self.perform_request(
            method="POST",
            path="/ws/oauth/token",
            params=params,
            # Note that we don't want any authentication on this
            # request, the 'code'/'refresh_token' is enough!
            http_auth=None,
        )


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
