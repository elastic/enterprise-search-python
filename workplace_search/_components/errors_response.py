from ..utils import typing
from ._base import JSONResponse


class ErrorsResponse(JSONResponse):
    @property
    def errors(self):
        # type: () -> typing.List[str]
        return self["errors"]
