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

from elastic_transport import APIError as APIError
from elastic_transport import BadGatewayError as BadGatewayError
from elastic_transport import BadRequestError as BadRequestError
from elastic_transport import ConflictError as ConflictError
from elastic_transport import ConnectionError as ConnectionError
from elastic_transport import ConnectionTimeout as ConnectionTimeout
from elastic_transport import ForbiddenError as ForbiddenError
from elastic_transport import GatewayTimeoutError as GatewayTimeoutError
from elastic_transport import InternalServerError as InternalServerError
from elastic_transport import MethodNotImplementedError as MethodNotImplementedError
from elastic_transport import NotFoundError as NotFoundError
from elastic_transport import PayloadTooLargeError as PayloadTooLargeError
from elastic_transport import PaymentRequiredError as PaymentRequiredError
from elastic_transport import SerializationError as SerializationError
from elastic_transport import ServiceUnavailableError as ServiceUnavailableError
from elastic_transport import TransportError as TransportError
from elastic_transport import UnauthorizedError as UnauthorizedError

from ._serializer import JSONSerializer
from ._version import __version__  # noqa: F401
from .client import AppSearch, EnterpriseSearch, WorkplaceSearch

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
    "SerializationError",
    "ServiceUnavailableError",
    "TransportError",
    "UnauthorizedError",
    "WorkplaceSearch",
]
