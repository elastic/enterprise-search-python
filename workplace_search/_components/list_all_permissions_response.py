from ..utils import typing
from ._base import JSONResponse
from .meta_page import MetaPage
from .permissions_user import PermissionsUser


class ListAllPermissionsResponse(JSONResponse):
    @property
    def meta(self):
        # type: () -> MetaPage
        return MetaPage(self["meta"])

    @property
    def results(self):
        # type: () -> typing.List[PermissionsUser]
        return [PermissionsUser(obj) for obj in self["results"]]
