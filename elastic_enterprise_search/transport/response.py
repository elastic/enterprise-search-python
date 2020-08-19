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


class Request(object):
    """HTTP request"""

    __slots__ = ("method", "path", "headers", "params")

    def __init__(self, method, path, headers, params):
        self.method = method
        self.path = path
        self.headers = headers
        self.params = params

    def __eq__(self, other):
        if isinstance(other, Request):
            return (
                self.method == other.method
                and self.path == other.path
                and self.headers == other.headers
                and self.params == other.params
            )
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Request):
            return (
                self.method != other.method
                or self.path != other.path
                or self.headers != other.headers
                or self.params != other.params
            )
        return NotImplemented


class Response(object):
    """HTTP response"""

    __slots__ = ("request", "status_code", "content")

    def __init__(self, request, status_code, content):
        self.request = request
        self.status_code = status_code
        self.content = content

    def __repr__(self):
        return repr(self.content)

    def __str__(self):
        return str(self.content)

    def __getattr__(self, item):
        return getattr(self.content, item)

    def __getitem__(self, item):
        return self.content[item]

    def __bool__(self):
        return bool(self.content)

    # Python 2 compatibility
    __nonzero__ = __bool__

    def __iter__(self):
        return iter(self.content)

    def __contains__(self, item):
        return item in self.content

    def __len__(self):
        return len(self.content)

    def __eq__(self, other):
        if isinstance(other, type(self.content)):
            return other == self.content
        elif isinstance(other, Response):
            return (
                self.status_code == other.status_code and self.content == other.content
            )
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self.content)):
            return other != self.content
        elif isinstance(other, Response):
            return (
                self.status_code != other.status_code or self.content != other.content
            )
        return NotImplemented
