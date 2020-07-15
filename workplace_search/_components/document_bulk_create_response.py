from ..utils import typing
from ._base import JSONResponse


class Items(dict):
    @property
    def id(self):
        # type: () -> str
        return self["id"]

    @property
    def errors(self):
        # type: () -> typing.List[str]
        return self["errors"]


class DocumentBulkCreateResponse(JSONResponse):
    @property
    def results(self):
        # type: () -> typing.List[Items]
        return [Items(obj) for obj in self["results"]]
