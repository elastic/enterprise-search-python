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

import datetime
import typing as t

from elastic_transport import ApiResponse, AsyncTransport
from elastic_transport.client_utils import percent_encode

from ..._utils import format_datetime

SKIP_IN_PATH = {None, "", b""}


def _escape(value: t.Any) -> str:
    if isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, datetime.datetime):
        return format_datetime(value)
    elif isinstance(value, bytes):
        return value.decode("utf-8", "surrogatepass")
    if not isinstance(value, str):
        return str(value)
    return value


def _quote(value: t.Any) -> str:
    return percent_encode(_escape(value), ",*[]:-")


def _quote_query(query: t.Mapping[str, t.Any]) -> str:
    kvs: t.List[t.Tuple[str, str]] = []
    for k, v in query.items():
        if isinstance(v, (list, tuple, dict)):
            if k.endswith("[]"):
                k = k[:-2]
            kvs.extend(_quote_query_deep_object(k, v))
        else:
            kvs.append((k, _quote(v)))

    return "&".join([f"{k}={v}" for k, v in kvs])


def _quote_query_deep_object(prefix, value) -> t.Iterable[t.Tuple[str, str]]:
    if not isinstance(value, (list, tuple, dict)):
        yield (prefix, _quote(value))
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _quote_query_deep_object(f"{prefix}[]", item)
    else:
        for key, val in value.items():
            yield from _quote_query_deep_object(f"{prefix}[{key}]", val)


class BaseClient:
    def __init__(self):
        self._transport = AsyncTransport()
        self._headers = None
        self._request_timeout = None
        self._max_retries = None
        self._retry_on_status = None
        self._retry_on_timeout = None
        self._client_meta = None

    @property
    def transport(self) -> AsyncTransport:
        return self._transport

    async def perform_request(
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

        resp = await self.transport.perform_request(
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
        return resp
