from ..utils import typing


class Document(dict):
    @property
    def id(self):
        # type: () -> typing.Optional[str]
        if self.get("id", None) is None:
            return None
        return self["id"]

    @property
    def _allow_permissions(self):
        # type: () -> typing.Optional[typing.List[str]]
        if self.get("_allow_permissions", None) is None:
            return None
        return self["_allow_permissions"]

    @property
    def _deny_permissions(self):
        # type: () -> typing.Optional[typing.List[str]]
        if self.get("_deny_permissions", None) is None:
            return None
        return self["_deny_permissions"]
