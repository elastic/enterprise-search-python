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

from elastic_transport import (
    ApiResponse,
    BaseNode,
    BinaryApiResponse,
    HeadApiResponse,
    HttpHeaders,
    ListApiResponse,
    ObjectApiResponse,
    TextApiResponse,
    Transport,
)
from elastic_transport.client_utils import DEFAULT, DefaultType

from ..._utils import (
    CLIENT_META_SERVICE,
    _quote_query,
    client_node_configs,
    resolve_auth_headers,
)
from ...exceptions import _HTTP_EXCEPTIONS, ApiError

_TYPE_SELF = t.TypeVar("_TYPE_SELF", bound="BaseClient")
_TYPE_HOSTS = t.Union[str, t.Dict[str, t.Any], t.List[str], t.List[t.Dict[str, t.Any]]]


class BaseClient:
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
        transport_class: t.Type[Transport] = Transport,
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
        _transport: t.Optional[Transport] = None,
    ):
        if _transport is None:
            transport_kwargs = {}
            if connections_per_node is not DEFAULT:
                transport_kwargs["connections_per_node"] = connections_per_node
            if http_compress is not DEFAULT:
                transport_kwargs["http_compress"] = http_compress
            if verify_certs is not DEFAULT:
                transport_kwargs["verify_certs"] = verify_certs
            if node_class is not DEFAULT:
                transport_kwargs["node_class"] = node_class
            if dead_node_backoff_factor is not DEFAULT:
                transport_kwargs["dead_node_backoff_factor"] = dead_node_backoff_factor
            if max_dead_node_backoff is not DEFAULT:
                transport_kwargs["max_dead_node_backoff"] = max_dead_node_backoff
            if meta_header is not DEFAULT:
                if not isinstance(meta_header, bool):
                    raise TypeError("meta_header must be of type bool")
                transport_kwargs["meta_header"] = meta_header

            node_configs = client_node_configs(
                hosts,
                connections_per_node=connections_per_node,
                http_compress=http_compress,
                verify_certs=verify_certs,
                ca_certs=ca_certs,
                client_cert=client_cert,
                client_key=client_key,
                ssl_assert_hostname=ssl_assert_hostname,
                ssl_assert_fingerprint=ssl_assert_fingerprint,
                ssl_version=ssl_version,
                ssl_context=ssl_context,
                ssl_show_warn=ssl_show_warn,
            )
            self._transport = transport_class(
                node_configs,
                client_meta_service=CLIENT_META_SERVICE,
                **transport_kwargs,
            )
        else:
            self._transport = _transport

        # Need to filter out the 'None' values
        headers = {
            k: v
            for k, v in resolve_auth_headers(
                headers=headers,
                http_auth=http_auth,
                basic_auth=basic_auth,
                bearer_auth=bearer_auth,
            ).items()
            if v is not None
        }
        self._headers = HttpHeaders(headers)

        self._request_timeout = request_timeout
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status
        self._retry_on_timeout = retry_on_timeout
        self._client_meta = DEFAULT
        self._ignore_status = None

    def __enter__(self: _TYPE_SELF) -> _TYPE_SELF:
        return self

    def __exit__(self, *_: t.Any) -> None:
        self.transport.close()

    @property
    def transport(self) -> Transport:
        return self._transport

    def options(
        self: _TYPE_SELF,
        *,
        opaque_id: t.Union[DefaultType, str] = DEFAULT,
        basic_auth: t.Union[DefaultType, str, t.Tuple[str, str]] = DEFAULT,
        bearer_auth: t.Union[DefaultType, str] = DEFAULT,
        headers: t.Union[DefaultType, t.Mapping[str, str]] = DEFAULT,
        request_timeout: t.Union[DefaultType, t.Optional[float]] = DEFAULT,
        ignore_status: t.Union[DefaultType, int, t.Collection[int]] = DEFAULT,
        max_retries: t.Union[DefaultType, int] = DEFAULT,
        retry_on_status: t.Union[DefaultType, int, t.Collection[int]] = DEFAULT,
        retry_on_timeout: t.Union[DefaultType, bool] = DEFAULT,
    ) -> _TYPE_SELF:
        client = type(self)(_transport=self.transport)

        resolved_headers = headers if headers is not DEFAULT else None
        resolved_headers = resolve_auth_headers(
            headers=resolved_headers,
            basic_auth=basic_auth,
            bearer_auth=bearer_auth,
        )
        if opaque_id is None:
            resolved_headers.pop("x-opaque-id", None)
        elif opaque_id is not DEFAULT:
            resolved_headers["x-opaque-id"] = opaque_id

        if resolved_headers:
            new_headers = self._headers.copy()
            for header, value in resolved_headers.items():
                if value is None:
                    new_headers.pop(header, None)
                else:
                    new_headers[header] = value
            client._headers = new_headers
        else:
            client._headers = self._headers.copy()

        if request_timeout is not DEFAULT:
            client._request_timeout = request_timeout

        if ignore_status is not DEFAULT:
            if isinstance(ignore_status, int):
                ignore_status = (ignore_status,)
            client._ignore_status = ignore_status

        if max_retries is not DEFAULT:
            if not isinstance(max_retries, int):
                raise TypeError("'max_retries' must be of type 'int'")
            client._max_retries = max_retries

        if retry_on_status is not DEFAULT:
            if isinstance(retry_on_status, int):
                retry_on_status = (retry_on_status,)
            client._retry_on_status = retry_on_status

        if retry_on_timeout is not DEFAULT:
            if not isinstance(retry_on_timeout, bool):
                raise TypeError("'retry_on_timeout' must be of type 'bool'")
            client._retry_on_timeout = retry_on_timeout

        return client

    def perform_request(
        self, method: str, path: str, params=None, headers=None, body=None
    ) -> ApiResponse:
        if headers:
            request_headers = self._headers.copy()
            request_headers.update(headers)
        else:
            request_headers = self._headers

        if params:
            request_target = f"{path}?{_quote_query(params)}"
        else:
            request_target = path

        resp = self.transport.perform_request(
            method,
            request_target,
            headers=request_headers,
            body=body,
            request_timeout=self._request_timeout,
            max_retries=self._max_retries,
            retry_on_status=self._retry_on_status,
            retry_on_timeout=self._retry_on_timeout,
            client_meta=self._client_meta,
        )

        # HEAD with a 404 is returned as a normal response
        # since this is used as an 'exists' functionality.
        if not 200 <= resp.meta.status < 299 and (
            self._ignore_status is DEFAULT
            or self._ignore_status is None
            or resp.meta.status not in self._ignore_status
        ):
            message = str(resp.body)

            raise _HTTP_EXCEPTIONS.get(resp.meta.status, ApiError)(
                message=message, meta=resp.meta, body=resp.body
            )

        if method == "HEAD":
            response = HeadApiResponse(meta=resp.meta)
        elif isinstance(resp.body, dict):
            response = ObjectApiResponse(body=resp.body, meta=resp.meta)  # type: ignore[assignment]
        elif isinstance(resp.body, list):
            response = ListApiResponse(body=resp.body, meta=resp.meta)  # type: ignore[assignment]
        elif isinstance(resp.body, str):
            response = TextApiResponse(  # type: ignore[assignment]
                body=resp.body,
                meta=resp.meta,
            )
        elif isinstance(resp.body, bytes):
            response = BinaryApiResponse(body=resp.body, meta=resp.meta)  # type: ignore[assignment]
        else:
            response = ApiResponse(body=resp.body, meta=resp.meta)  # type: ignore[assignment]

        return response
