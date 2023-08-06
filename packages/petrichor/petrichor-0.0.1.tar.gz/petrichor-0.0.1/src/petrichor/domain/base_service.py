"""This module is a base service class."""

import asyncpg
import pydantic

from petrichor.core.exceptions import http_exceptions
from petrichor.core.singleton_meta import SingletonMeta
from petrichor.domain import base_schemas


class BaseService(metaclass=SingletonMeta):
    def __init__(self, queries, schemas):
        self._queries = queries
        self._schemas = schemas

    async def create(self, request):
        """Add a new entry.

        Raises:
            Conflict: Is raised if an entry like that already exists.

        Returns:
            DB schema version of the object.
        """
        try:
            new_model = await self._queries.create(request)
        except asyncpg.exceptions.UniqueViolationError:
            raise http_exceptions.Conflict("Such an entry already exists.")

        return self._schemas.DB.from_orm(new_model)

    async def get_list(self, page: int, page_size: int, **kwargs) -> base_schemas.Paginated:
        """Get a paginated result list of entries."""
        paginated_response = await self._queries.paginated_list(page=page, page_size=page_size, **kwargs)
        transformed_results = [self._schemas.DB.from_orm(result_row) for result_row in paginated_response.result_list]
        pagination = base_schemas.Pagination(total=paginated_response.total, more=paginated_response.more)
        return base_schemas.Paginated(results=transformed_results, pagination=pagination)

    async def get_by_id(self, identifier: pydantic.UUID4):
        """Get the entry that matches the primary key (identifier).

        Returns:
            DB schema version of the object.
        """
        db_object = await self._queries.get_by_pk(identifier=identifier)
        return self._schemas.DB.from_orm(db_object)
