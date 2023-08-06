from typing import Any


class PaginatedQueryResponse:
    def __init__(self, total: int, page_size: int, page, result_list: list[Any]):
        self.result_list = result_list
        self.more: bool = (total / page_size) > page
        self.total: int = total


class BaseQueries:  # noqa: WPS214
    def __init__(self, model, db) -> None:
        self.model = model
        self.DB = db

    async def create(self, request):
        """Persist the Request Schema to the database.

        Args:
            request: Pydantic schema of the model.

        Returns:
            The created model
        """
        return await self.model.create(**dict(request))

    async def paginated_list(self, page_size: int, page: int, **filters) -> PaginatedQueryResponse:
        pruned_filter = self._prune_filter(**filters)
        paginated_result = await self._paginate_query(page_size, page, **pruned_filter)
        count = await self._count_query(**pruned_filter)
        return PaginatedQueryResponse(count, page_size, page, paginated_result)

    async def all(self, **filters) -> list[Any]:
        """Get all entries matching optional filters."""
        pruned_filter = self._prune_filter(**filters)
        query = self._filter(query=self.model.query, **pruned_filter)
        query = self._order(query)
        return await query.gino.all()

    async def get_by_pk(self, identifier):
        """Search by primary key.

        Returns:
            Model
        """
        return await self.model.get(identifier)

    @property
    def _order_key(self):
        return self.model.name

    @property
    def _pk(self):
        return self.model.identifier

    def _paginate(self, query, page_size: int, page: int):
        return query.offset(page_size * (page - 1)).limit(page_size)

    def _order(self, query):
        return query.order_by(self._order_key.asc())

    def _filter(self, query, **filters):
        for filter_key, filter_value in filters.items():
            query = query.where(getattr(self.model, filter_key) == filter_value)
        return query

    def _prune_filter(self, **filters):
        pruned_filter = {}
        for filter_name, filter_value in filters.items():
            if filter_value is not None:
                pruned_filter[filter_name] = filter_value
        return pruned_filter

    async def _count_query(self, **filters):
        if filters:
            query = self.DB.select([self.DB.func.count()])
            query = self._filter(query, **filters)
        else:
            query = self.DB.func.count(self._pk)
        return await query.gino.scalar()

    async def _paginate_query(self, page_size: int, page: int, **filters):
        query = self._filter(self.model.query, **filters)
        ordered_query = self._order(query)
        ppaginated_query = self._paginate(ordered_query, page_size, page)
        return await ppaginated_query.gino.all()
