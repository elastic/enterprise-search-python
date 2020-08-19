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

from six import add_metaclass, python_2_unicode_compatible


HTTP_EXCEPTIONS = {}


class EnterpriseSearchErrorMeta(type):
    def __new__(meta_cls, *args, **kwargs):
        # Gather all the subclasses of 'EnterpriseSearchError'
        # and categorize them by status_code.
        cls = type.__new__(meta_cls, *args, **kwargs)
        status_code = getattr(cls, "status_code", None)
        if status_code is not None:
            HTTP_EXCEPTIONS[status_code] = cls
        return cls


@python_2_unicode_compatible
@add_metaclass(EnterpriseSearchErrorMeta)
class EnterpriseSearchError(Exception):
    """Generic exception for the 'elastic-enterprise-search' package"""

    status_code = None

    def __init__(self, message, errors=(), status_code=None):
        super(EnterpriseSearchError, self).__init__(message)
        self._errors = errors
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    @property
    def errors(self):
        return list(self._errors)

    def __repr__(self):
        parts = [self.__class__.__name__]
        if self.status_code:
            parts.append(str(self.status_code))
        parts.append(self.message)
        return " ".join(parts)

    def __str__(self):
        if self.status_code:
            return "%s %s" % (self.status_code, self.message)
        return str(self.message)


class SerializationError(EnterpriseSearchError):
    """Error that occurred during the serialization or
    deserialization of an HTTP message body
    """


class TransportError(EnterpriseSearchError):
    """Base class for errors raised by the Transport or Connection"""


class ConnectionError(TransportError):
    """Error raised by the HTTP connection"""


class ConnectionTimeout(TransportError):
    """Connection timed out during an operation"""


class RetriesExhausted(TransportError):
    """All retries have been attempted and the operation hasn't succeeded
    Returns with all errors that occurred throughout the retry lifecycle
    in order of most recent occurrence to oldest occurence
    """


class APIError(TransportError):
    """Error that is raised from the service via HTTP status codes"""


class BadRequest(APIError):
    """Error for HTTP status 400 'Bad Request'"""

    status_code = 400


class Unauthorized(APIError):
    """Error for HTTP status 401 'Unauthorized'"""

    status_code = 401


class PaymentRequired(APIError):
    """Error for HTTP status 402 'Payment Required'
    Usually signals that your instance doesn't have
    a proper license active for the operation
    """

    status_code = 402


class Forbidden(APIError):
    """Error for HTTP status 403 'Forbidden'"""

    status_code = 403


class NotFound(APIError):
    """Error for HTTP status 404 'Not Found'"""

    status_code = 404


class Conflict(APIError):
    """Error for HTTP status 409 'Conflict'"""

    status_code = 409


class PayloadTooLarge(APIError):
    """Error for HTTP status 413 'Payload Too Large'"""

    status_code = 413


class InternalServerError(APIError):
    """Error for HTTP status 500 'Internal Server Error'"""

    status_code = 500


class MethodNotImplemented(APIError):
    """Error for HTTP status 501 'Method Not Allowed'"""

    status_code = 501


class BadGateway(APIError):
    """Error for HTTP status 502 'Bad Gateway'"""

    status_code = 502


class ServiceUnavailable(APIError):
    """Error for HTTP status 503 'Service Unavailable'"""

    status_code = 503


class GatewayTimeout(APIError):
    """Error for HTTP status 504 'Gateway Timeout'"""

    status_code = 504
