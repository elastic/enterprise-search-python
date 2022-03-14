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
import warnings

from elastic_transport import ApiError as _ApiError


class ApiError(_ApiError):
    @property
    def status(self) -> int:
        warnings.warn(
            "ApiError.status is deprecated in favor of ApiError.meta.status",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.meta.status


class BadGatewayError(ApiError):
    pass


class BadRequestError(ApiError):
    pass


class ConflictError(ApiError):
    pass


class ForbiddenError(ApiError):
    pass


class GatewayTimeoutError(ApiError):
    pass


class InternalServerError(ApiError):
    pass


class NotFoundError(ApiError):
    pass


class PayloadTooLargeError(ApiError):
    pass


class ServiceUnavailableError(ApiError):
    pass


class UnauthorizedError(ApiError):
    pass


_HTTP_EXCEPTIONS: t.Dict[int, ApiError] = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    413: PayloadTooLargeError,
    500: InternalServerError,
    502: BadGatewayError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
}
