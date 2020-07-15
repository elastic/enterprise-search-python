from ..utils import typing
from ._base import JSONResponse
from .external_identity import ExternalIdentity
from .meta_page import MetaPage


class ListAllExternalIdentitiesResponse(JSONResponse):
    @property
    def meta(self):
        # type: () -> MetaPage
        return MetaPage(self["meta"])

    @property
    def results(self):
        # type: () -> typing.List[ExternalIdentity]
        return [ExternalIdentity(obj) for obj in self["results"]]
