from ..utils import typing


class PermissionsUser(dict):
    @property
    def user(self):
        # type: () -> str
        return self["user"]

    @property
    def permissions(self):
        # type: () -> typing.List[str]
        return self["permissions"]
