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

import base64
from six import ensure_str, ensure_binary, ensure_text
from ..transport import Transport


__all__ = ["BaseClient"]


class BaseClient(object):
    def __init__(
        self,
        hosts=None,
        http_auth=None,
        transport_class=None,
        _transport=None,
        **kwargs
    ):
        if _transport is not None:
            if transport_class is not None or any(
                v is not None for v in kwargs.values()
            ):
                raise ValueError(
                    "Can't pass both a Transport and parameters to a client"
                )
            self.transport = _transport
        else:
            self.transport = (transport_class or Transport)(hosts, **kwargs)

        # Clients hold on to their own 'Authorization' HTTP header
        # because Enterprise, Workplace, and App Search all have
        # their own authentication schemes and can be authenticated
        # separately while sharing a Transport layer.
        self._auth_header = None
        if http_auth is not None:
            self.http_auth = http_auth

    def close(self):
        self.transport.close()

    @property
    def http_auth(self):
        auth_header = self._auth_header
        if auth_header:
            # We split basic auth into a tuple if we can
            if auth_header.startswith("Basic "):
                try:
                    b64_encoded = ensure_binary(auth_header.partition(" ")[-1])
                    b64_decoded = ensure_text(base64.b64decode(b64_encoded))
                    return tuple(b64_decoded.split(":", 1))
                except Exception:
                    pass
            return auth_header.partition(" ")[-1]
        return None

    @http_auth.setter
    def http_auth(self, http_auth):
        self._auth_header = self._parse_http_auth(http_auth)

    @staticmethod
    def _parse_http_auth(http_auth):
        # Basic auth with (username, password)
        if isinstance(http_auth, (tuple, list)) and len(http_auth) == 2:
            basic_auth = ensure_str(
                base64.b64encode((b":".join([ensure_binary(x) for x in http_auth])))
            )
            return "Basic %s" % basic_auth

        # If not a tuple/list or string raise an error.
        elif not isinstance(http_auth, str):
            raise TypeError(
                "'http_auth' must either be a tuple of (username, password) "
                "for 'Basic' authentication or a single string for "
                "'Bearer'/token authentication"
            )

        # Bearer / Token auth
        else:
            return "Bearer %s" % http_auth

    def _perform_request(
        self, method, path, headers=None, params=None, body=None, http_auth=None
    ):
        """Adds client authentication to request headers
        before handing it to the Transport layer.
        """
        request_headers = (headers or {}).copy()
        if self._auth_header or http_auth:
            if http_auth:
                auth_header = self._parse_http_auth(http_auth)
            else:
                auth_header = self._auth_header
            for key, val in request_headers.items():
                request_headers[key.lower()] = val
            request_headers.setdefault("authorization", auth_header)

        return self.transport.perform_request(
            method, path, headers=request_headers, params=params, body=body
        )

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
