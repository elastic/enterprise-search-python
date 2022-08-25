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

import re

from elastic_transport import ConnectionError as ConnectionError
from elastic_transport import ConnectionTimeout as ConnectionTimeout
from elastic_transport import SerializationError as SerializationError
from elastic_transport import TransportError as TransportError
from elastic_transport import __version__ as _elastic_transport_version

from ._async.client import AsyncAppSearch as AsyncAppSearch
from ._async.client import AsyncEnterpriseSearch as AsyncEnterpriseSearch
from ._async.client import AsyncWorkplaceSearch as AsyncWorkplaceSearch
from ._serializer import JsonSerializer
from ._sync.client import AppSearch as AppSearch
from ._sync.client import EnterpriseSearch as EnterpriseSearch
from ._sync.client import WorkplaceSearch as WorkplaceSearch
from ._version import __version__  # noqa: F401
from .exceptions import (
    ApiError,
    BadGatewayError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    GatewayTimeoutError,
    InternalServerError,
    NotFoundError,
    PayloadTooLargeError,
    ServiceUnavailableError,
    UnauthorizedError,
)

# Ensure that a compatible version of elastic-transport is installed.
_version_groups = tuple(int(x) for x in re.search(r"^(\d+)\.(\d+)\.(\d+)", _elastic_transport_version).groups())  # type: ignore
if _version_groups < (8, 4, 0) or _version_groups > (9, 0, 0):
    raise ImportError(
        "An incompatible version of elastic-transport is installed. Must be between "
        "v8.4.0 and v9.0.0. Install the correct version with the following command: "
        "$ python -m pip install 'elastic-transport>=8.4, <9'"
    )

__all__ = [
    "ApiError",
    "AppSearch",
    "AsyncAppSearch",
    "AsyncEnterpriseSearch",
    "AsyncWorkplaceSearch",
    "BadGatewayError",
    "BadRequestError",
    "ConflictError",
    "ConnectionError",
    "ConnectionTimeout",
    "EnterpriseSearch",
    "ForbiddenError",
    "GatewayTimeoutError",
    "InternalServerError",
    "JsonSerializer",
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

# Aliases for compatibility with 7.x
APIError = ApiError
JSONSerializer = JsonSerializer
