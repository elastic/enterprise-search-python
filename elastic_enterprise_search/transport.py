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

from platform import python_version
import requests
import six
from six.moves.urllib.parse import urljoin
from ._version import __version__
from .exceptions import HTTP_EXCEPTIONS, HTTPError, ConnectionError


class BaseResponse(object):
    """Base class for HTTP responses"""

    def __init__(self, status_code, headers):
        self.status_code = status_code
        self.headers = headers


class TextResponse(BaseResponse, str):
    """HTTP responses that are not JSON"""

    def __init__(self, status_code, headers, body):
        print(status_code, headers, body)
        BaseResponse.__init__(self, status_code, headers)
        str.__init__(self, body)


class JSONResponse(BaseResponse, dict):
    """HTTP responses that are JSON"""

    def __init__(self, status_code, headers, body):
        BaseResponse.__init__(self, status_code, headers)
        dict.__init__(self, body)


class Transport(object):
    def __init__(self, host=None, port=None, use_ssl=None, headers=None):
        if host is None:
            host = "localhost"
            if port is None:
                port = 3002

        authority = host
        if port is not None:
            if ":" in authority:  # IPv6
                authority = "[%s]:%d" % (authority, port)
            else:
                authority = "%s:%d" % (authority, port)
        scheme = "https" if use_ssl else "http"
        self._base_url = "%s://%s" % (scheme, authority)
        self._session = requests.Session()

        self.headers = {k.lower(): v for k, v in (headers or {}).items()}
        self.headers.setdefault(
            "user-agent",
            "enterprise-search-python/%s (Python %s)" % (__version__, python_version()),
        )
        self.headers.setdefault("accept", "application/json")
        self.headers.setdefault("accept-encoding", "gzip")

    def request(self, method, path, body=None, headers=None, params=None):
        url = urljoin(self._base_url, path)
        if headers:
            request_headers = self.headers.copy()
            request_headers.update(headers)
        else:
            request_headers = self.headers
        if isinstance(body, (str, bytes)):
            request_kwargs = {"data": body}
        else:
            request_kwargs = {"json": body}

        # Send our request and reraise any errors
        # we receive from Requests as ConnectionErrors.
        try:
            resp = self._session.request(
                method, url, headers=request_headers, params=params, **request_kwargs
            )
            # Try parsing as JSON, if not use the text.
            # We can potentially get encoding errors here
            # but that'd probably mean there's a bad
            # proxy or something strange like that?
            try:
                body = resp.json()
            except Exception:
                body = resp.text
        except (requests.ConnectionError, UnicodeError) as e:
            return six.raise_from(ConnectionError(error=e), None)

        # We've got a successful response here, now
        # we either return a response or raise an HTTPError.
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            error_cls = HTTP_EXCEPTIONS.get(resp.status_code, HTTPError)
            return six.raise_from(
                error_cls(
                    status_code=resp.status_code, headers=resp.headers.copy(), body=body
                ),
                None,
            )

        if isinstance(body, str):
            return TextResponse(resp.status_code, resp.headers.copy(), body)
        else:
            return JSONResponse(resp.status_code, resp.headers.copy(), body)

    def copy(self):
        """Returns a copy of the Transport that is disjoint in all
        public properties like 'headers' but share a Requests Session
        for better connection pooling across clients.
        """
        transport = Transport()
        transport.headers = self.headers.copy()
        transport._session = self._session
        transport._base_url = self._base_url
        return transport
