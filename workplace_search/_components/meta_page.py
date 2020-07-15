class Page(dict):
    @property
    def current(self):
        # type: () -> int
        return self["current"]

    @property
    def total_pages(self):
        # type: () -> int
        return self["total_pages"]

    @property
    def total_results(self):
        # type: () -> int
        return self["total_results"]

    @property
    def size(self):
        # type: () -> int
        return self["size"]


class MetaPage(dict):
    @property
    def page(self):
        # type: () -> Page
        return Page(self["page"])
