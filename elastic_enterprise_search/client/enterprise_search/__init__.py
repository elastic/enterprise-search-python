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

from ..utils import SKIP_IN_PATH, BaseClient, JSONResponse, make_path, make_params


class EnterpriseSearch(BaseClient):
    def get_health(
        self, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Get information on the health of a deployment and basic statistics around
        resource usage
        
        """

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "ent", "v1", "internal", "health"),
                params=params,
                headers=headers,
            )
        )

    def get_read_only(
        self, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Get the read-only flag's state
        
        """

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "ent", "v1", "internal", "read_only_mode"),
                params=params,
                headers=headers,
            )
        )

    def put_read_only(
        self, body, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Update the read-only flag's state
        
        """

        return JSONResponse(
            *self.transport.request(
                "PUT",
                make_path("api", "ent", "v1", "internal", "read_only_mode"),
                body=body,
                params=params,
                headers=headers,
            )
        )

    def get_stats(
        self, include=None, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Get information about the resource usage of the application, the state of
        different internal queues, etc.
        
        :arg include: Comma-separated list of stats to return
        """

        params = make_params(params, {"include": include})
        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "ent", "v1", "internal", "stats"),
                params=params,
                headers=headers,
            )
        )

    def get_version(
        self, params=None, headers=None,
    ):
        # type: (...) -> JSONResponse
        """
        Get version information for this server
        
        """

        return JSONResponse(
            *self.transport.request(
                "GET",
                make_path("api", "ent", "v1", "internal", "version"),
                params=params,
                headers=headers,
            )
        )
