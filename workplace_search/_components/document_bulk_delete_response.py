from ..utils import typing
from ._base import JSONResponse


class Items(dict):
    @property
    def id(self):
        # type: () -> str
        return self["id"]

    @property
    def success(self):
        # type: () -> bool
        return self["success"]


class DocumentBulkDeleteResponse(JSONResponse):
    @property
    def results(self):
        # type: () -> typing.List[Items]
        return [Items(obj) for obj in self["results"]]
