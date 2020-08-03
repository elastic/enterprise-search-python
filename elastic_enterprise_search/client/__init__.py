import jwt
from .app_search import AppSearch as _AppSearch
from .enterprise_search import EnterpriseSearch as _EnterpriseSearch
from .workplace_search import WorkplaceSearch as _WorkplaceSearch

__all__ = ["AppSearch", "EnterpriseSearch", "WorkplaceSearch"]


class AppSearch(_AppSearch):
    """Client for Elastic App Search service
    `<https://www.elastic.co/guide/en/app-search/current/api-reference.html>`_
    """

    @staticmethod
    def create_signed_search_key(
        api_key,
        api_key_name,
        search_fields=None,
        result_fields=None,
        filters=None,
        facets=None,
    ):
        """Creates a Signed Search Key to keep your Private API Key secret
        and restrict what a user can search over.

        `<https://www.elastic.co/guide/en/app-search/current/authentication.html#authentication-signed>`_

        :arg api_key: Private API Key
        :arg api_key_name: Name of the Signed Search Key
        :arg search_fields: Fields to search over.
        :arg result_fields: Fields to return in the result
        :arg filters: Adds filters to the search requests
        :arg facets: Sets the facets that are allowed.
            To disable aggregations set to '{}' or 'None'.
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


class WorkplaceSearch(_WorkplaceSearch):
    """Client for Workplace Search
    `<https://www.elastic.co/guide/en/workplace-search/current/workplace-search-api-overview.html>`_
    """


class EnterpriseSearch(_EnterpriseSearch):
    """Client for Enterprise Search"""

    def __init__(self, transport_class=None, **kwargs):
        super(EnterpriseSearch, self).__init__(
            transport_class=transport_class, **kwargs
        )

        self.app_search = AppSearch(_transport=self.transport.copy())
        self.workplace_search = WorkplaceSearch(_transport=self.transport.copy())
