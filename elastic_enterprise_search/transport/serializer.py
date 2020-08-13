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

try:
    import simplejson as json
except ImportError:
    import json

import uuid
from datetime import date, datetime
from decimal import Decimal
import six

from ..exceptions import SerializationError
from ..utils import string_types, format_datetime

FLOAT_TYPES = (Decimal,)
DATE_TYPES = (date,)
DATETIME_TYPES = (datetime,)


class TextSerializer(object):
    mimetype = "text/plain"

    def loads(self, s):
        return s

    def dumps(self, data):
        if isinstance(data, string_types):
            return data
        raise SerializationError("Cannot serialize %r into text" % data)


class JSONSerializer(object):
    mimetype = "application/json"

    def default(self, data):
        if isinstance(data, DATE_TYPES):
            return data.isoformat()
        elif isinstance(data, DATETIME_TYPES):
            return format_datetime(data)
        elif isinstance(data, uuid.UUID):
            return str(data)
        elif isinstance(data, FLOAT_TYPES):
            return float(data)
        raise SerializationError(
            "Unable to serialize %r (type: %s)" % (data, type(data))
        )

    def loads(self, s):
        try:
            return json.loads(s)
        except (ValueError, TypeError) as e:
            raise SerializationError(message=s, errors=(e,))

    def dumps(self, data):
        if isinstance(data, string_types):
            return data
        try:
            return json.dumps(
                data, default=self.default, ensure_ascii=False, separators=(",", ":")
            )
        except (ValueError, TypeError) as e:
            raise SerializationError(message=data, errors=(e,))


DEFAULT_SERIALIZERS = {
    JSONSerializer.mimetype: JSONSerializer(),
    TextSerializer.mimetype: TextSerializer(),
}


class Deserializer(object):
    def __init__(self, serializers, default_mimetype="application/json"):
        try:
            self.default = serializers[default_mimetype]
        except KeyError:
            raise ValueError("Cannot find default serializer (%s)" % default_mimetype)
        self.serializers = serializers

    def loads(self, s, mimetype=None):
        if not mimetype:
            deserializer = self.default
        else:
            # split out charset
            mimetype, _, _ = mimetype.partition(";")
            try:
                deserializer = self.serializers[mimetype]
            except KeyError:
                return six.raise_from(
                    SerializationError(
                        "Unknown mimetype, unable to deserialize: %s" % mimetype
                    ),
                    None,
                )

        return deserializer.loads(s)
