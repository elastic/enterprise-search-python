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
from urllib.parse import urlencode

import jwt
from elastic_transport import AsyncTransport, BaseNode
from elastic_transport.client_utils import DEFAULT, DefaultType

from ._base import _TYPE_HOSTS
from .app_search import AsyncAppSearch as _AsyncAppSearch
from .enterprise_search import AsyncEnterpriseSearch as _AsyncEnterpriseSearch
from .workplace_search import AsyncWorkplaceSearch as _AsyncWorkplaceSearch


class AsyncAppSearch(_AsyncAppSearch):
    """Client for App Search

    `<https://www.elastic.co/guide/en/app-search/current/api-reference.html>`_
    """

    @staticmethod
    def create_signed_search_key(
        *,
        api_key: str,
        api_key_name: str,
        search_fields: t.Optional[t.Dict[str, t.Any]] = DEFAULT,
        result_fields: t.Optional[t.Dict[str, t.Any]] = DEFAULT,
        filters: t.Optional[t.Dict[str, t.Any]] = DEFAULT,
        facets: t.Optional[t.Dict[str, t.Any]] = DEFAULT,
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
        return jwt.encode(payload=options, key=api_key, algorithm="HS256")


class AsyncWorkplaceSearch(_AsyncWorkplaceSearch):
    """Client for Workplace Search

    `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-api-overview.html>`_
    """

    def oauth_authorize_url(
        self, *, response_type: str, client_id: str, redirect_uri: str
    ) -> str:
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

        # Get a random node from the pool to use as a base URL.
        base_url = self.transport.node_pool.get().base_url.rstrip("/")
        query = urlencode(
            [
                ("response_type", response_type),
                ("client_id", client_id),
                ("redirect_uri", redirect_uri),
            ]
        )
        return f"{base_url}/ws/oauth/authorize?{query}"

    async def oauth_exchange_for_access_token(
        self,
        *,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code: t.Optional[str] = None,
        refresh_token: t.Optional[str] = None,
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

        params = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        if code is not None:
            params["code"] = code
        else:
            params["refresh_token"] = refresh_token

        return await self.options(headers={"Authorization": None}).perform_request(
            method="POST",
            path="/ws/oauth/token",
            params=params,
        )


class AsyncEnterpriseSearch(_AsyncEnterpriseSearch):
    def __init__(
        self,
        hosts: t.Optional[_TYPE_HOSTS] = None,
        *,
        # API
        basic_auth: t.Optional[t.Union[str, t.Tuple[str, str]]] = DEFAULT,
        bearer_auth: t.Optional[str] = DEFAULT,
        # Node
        headers: t.Union[DefaultType, t.Mapping[str, str]] = DEFAULT,
        connections_per_node: t.Union[DefaultType, int] = DEFAULT,
        http_compress: t.Union[DefaultType, bool] = DEFAULT,
        verify_certs: t.Union[DefaultType, bool] = DEFAULT,
        ca_certs: t.Union[DefaultType, str] = DEFAULT,
        client_cert: t.Union[DefaultType, str] = DEFAULT,
        client_key: t.Union[DefaultType, str] = DEFAULT,
        ssl_assert_hostname: t.Union[DefaultType, str] = DEFAULT,
        ssl_assert_fingerprint: t.Union[DefaultType, str] = DEFAULT,
        ssl_version: t.Union[DefaultType, int] = DEFAULT,
        ssl_context: t.Union[DefaultType, t.Any] = DEFAULT,
        ssl_show_warn: t.Union[DefaultType, bool] = DEFAULT,
        # Transport
        transport_class: t.Type[AsyncTransport] = AsyncTransport,
        request_timeout: t.Union[DefaultType, None, float] = DEFAULT,
        node_class: t.Union[DefaultType, t.Type[BaseNode]] = DEFAULT,
        dead_node_backoff_factor: t.Union[DefaultType, float] = DEFAULT,
        max_dead_node_backoff: t.Union[DefaultType, float] = DEFAULT,
        max_retries: t.Union[DefaultType, int] = DEFAULT,
        retry_on_status: t.Union[DefaultType, int, t.Collection[int]] = DEFAULT,
        retry_on_timeout: t.Union[DefaultType, bool] = DEFAULT,
        meta_header: t.Union[DefaultType, bool] = DEFAULT,
        # Deprecated
        http_auth: t.Optional[t.Union[str, t.Tuple[str, str]]] = DEFAULT,
        # Internal
        _transport: t.Optional[AsyncTransport] = None,
    ):
        super().__init__(
            hosts,
            basic_auth=basic_auth,
            bearer_auth=bearer_auth,
            headers=headers,
            connections_per_node=connections_per_node,
            http_compress=http_compress,
            verify_certs=verify_certs,
            ca_certs=ca_certs,
            client_cert=client_cert,
            client_key=client_key,
            ssl_assert_fingerprint=ssl_assert_fingerprint,
            ssl_assert_hostname=ssl_assert_hostname,
            ssl_version=ssl_version,
            ssl_context=ssl_context,
            ssl_show_warn=ssl_show_warn,
            transport_class=transport_class,
            request_timeout=request_timeout,
            retry_on_status=retry_on_status,
            retry_on_timeout=retry_on_timeout,
            max_retries=max_retries,
            node_class=node_class,
            dead_node_backoff_factor=dead_node_backoff_factor,
            max_dead_node_backoff=max_dead_node_backoff,
            meta_header=meta_header,
            http_auth=http_auth,
            _transport=_transport,
        )

        self.app_search = AsyncAppSearch(_transport=self.transport)
        self.workplace_search = AsyncWorkplaceSearch(_transport=self.transport)
