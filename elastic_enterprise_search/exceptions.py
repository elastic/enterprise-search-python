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


class EnterpriseSearchError(Exception):
    """Generic exception for the 'elastic-enterprise-search' package"""

    def __init__(self, error=None):
        self.error = error

    def __repr__(self):
        params = {
            k: getattr(self, k, None)
            for k in ("status_code", "error", "body", "headers")
        }
        params = ", ".join("%s=%r" % (k, v) for k, v in params.items() if v is not None)
        return "<%s(%s)>" % (type(self).__name__, params)

    __str__ = __repr__


class TransportError(EnterpriseSearchError):
    """Exception for all errors related to the Transport"""


class ConnectionError(TransportError):
    """Exception related to the underlying socket connection"""


class TLSError(ConnectionError):
    """Exception related to TLS/SSL"""


class HTTPError(TransportError):
    """Error that is raised from a non-2XX HTTP response"""

    def __init__(self, status_code, headers, body, error=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        super(HTTPError, self).__init__(error=error)


class BadRequestError(HTTPError):
    """Exception that's raised for 400 HTTP responses"""


class UnauthorizedError(HTTPError):
    """Exception that's raised for 401 HTTP responses"""


class ForbiddenError(HTTPError):
    """Exception that's raised for 403 HTTP responses"""


class NotFoundError(HTTPError):
    """Exception that's raised for 404 HTTP responses"""


class ConflictError(HTTPError):
    """Exception that's raised for 409 HTTP responses"""


HTTP_EXCEPTIONS = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
}
