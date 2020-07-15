class ExternalIdentity(dict):
    @property
    def source_user_id(self):
        # type: () -> str
        return self["source_user_id"]

    @property
    def user(self):
        # type: () -> str
        return self["user"]
