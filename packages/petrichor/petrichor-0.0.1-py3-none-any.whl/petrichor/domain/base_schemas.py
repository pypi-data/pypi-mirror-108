import pydantic


class Pagination(pydantic.BaseModel):  # noqa: H601
    """Common pagination pydantic model."""

    more: bool
    total: int


class Paginated(pydantic.BaseModel):
    """Paginated result schema."""

    results: list  # noqa: WPS110
    pagination: Pagination
