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

"""Python Elastic Enterprise Search Client"""

from elastic_transport import (
    APIError,
    BadRequestError,
    BadGatewayError,
    PaymentRequiredError,
    UnauthorizedError,
    ServiceUnavailableError,
    InternalServerError,
    MethodNotImplementedError,
    NotFoundError,
    ForbiddenError,
    GatewayTimeoutError,
    ConflictError,
    SerializationError,
    RetriesExhausted,
    ConnectionError,
    ConnectionTimeout,
    TransportError,
    PayloadTooLargeError,
)
from .client import AppSearch, EnterpriseSearch, WorkplaceSearch
from .serializer import JSONSerializer
from ._version import __version__  # noqa: F401
from .utils import parse_datetime

__all__ = [
    "APIError",
    "AppSearch",
    "BadGatewayError",
    "BadRequestError",
    "ConflictError",
    "ConnectionError",
    "ConnectionTimeout",
    "EnterpriseSearch",
    "ForbiddenError",
    "GatewayTimeoutError",
    "InternalServerError",
    "JSONSerializer",
    "MethodNotImplementedError",
    "NotFoundError",
    "PayloadTooLargeError",
    "PaymentRequiredError",
    "RetriesExhausted",
    "SerializationError",
    "ServiceUnavailableError",
    "TransportError",
    "UnauthorizedError",
    "WorkplaceSearch",
    "parse_datetime",
]
