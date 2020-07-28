from .app_search import AppSearch as AppSearch
from .enterprise_search import EnterpriseSearch as _EnterpriseSearch
from .workplace_search import WorkplaceSearch as WorkplaceSearch

__all__ = ["AppSearch", "EnterpriseSearch", "WorkplaceSearch"]


class EnterpriseSearch(_EnterpriseSearch):
    def __init__(self, transport_class=None, **kwargs):
        super(EnterpriseSearch, self).__init__(
            transport_class=transport_class, **kwargs
        )

        self.app_search = AppSearch(_transport=self.transport.copy())
        self.workplace_search = WorkplaceSearch(_transport=self.transport.copy())
