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

from elastic_transport import JSONSerializer as _JSONSerializer

from ._utils import format_datetime


class JSONSerializer(_JSONSerializer):
    """Same as elastic_transport.JSONSerializer except also formats
    datetime objects to RFC 3339. If a datetime is received without
    explicit timezone information then the timezone will be assumed
    to be the local timezone.
    """

    def default(self, data):
        if isinstance(data, datetime.datetime):
            return format_datetime(data)
        return super(JSONSerializer, self).default(data)
