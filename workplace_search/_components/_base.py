from typing import Mapping, Any


class Response(object):
    def __init__(self, status_code: int, headers: Mapping[str, str], body: Any):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __eq__(self, other):
        if not isinstance(other, Response):
            return NotImplemented
        return (
            self.status_code == other.status_code
            and self.headers == other.headers
            and self.body == other.body
        )

    def __ne__(self, other):
        if not isinstance(other, Response):
            return NotImplemented
        return not self == other

    def __repr__(self):
        return "<Response(status_code=%d headers=%r body=%r)>" % (
            self.status_code,
            self.headers,
            self.body,
        )


class JSONResponse(Response, dict):
    def __init__(self, status_code: int, headers: Mapping[str, str], body: Any):
        self.status_code = status_code
        self.headers = headers
        self.body = body

        dict.__init__(self, body)
