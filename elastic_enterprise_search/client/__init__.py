import jwt
from .app_search import AppSearch as _AppSearch
from .enterprise_search import EnterpriseSearch as _EnterpriseSearch
from .workplace_search import WorkplaceSearch as WorkplaceSearch

__all__ = ["AppSearch", "EnterpriseSearch", "WorkplaceSearch"]


class AppSearch(_AppSearch):
    @staticmethod
    def create_signed_search_key(
        api_key,
        api_key_name,
        search_fields=None,
        result_fields=None,
        filters=None,
        facets=None,
    ):
        """Creates a signed search key to keep your Private API Key secret
        and restrict what a user can search over.

        `<https://swiftype.com/documentation/app-search/authentication#signed>`_

        :arg api_key:
        :arg api_key_name:
        :arg search_fields:
        :arg result_fields:
        :arg filters:
        :arg facets:
        """
        options = {
            k: v
            for k, v in (
                ("api_key_name", api_key_name),
                ("search_fields", search_fields),
                ("result_fields", result_fields),
                ("filters", filters),
                ("facets", facets),
            )
            if v is not None
        }
        return jwt.encode(payload=options, key=api_key, algorithm="HS256")


class EnterpriseSearch(_EnterpriseSearch):
    def __init__(self, transport_class=None, **kwargs):
        super(EnterpriseSearch, self).__init__(
            transport_class=transport_class, **kwargs
        )

        self.app_search = AppSearch(_transport=self.transport.copy())
        self.workplace_search = WorkplaceSearch(_transport=self.transport.copy())
