from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Paginated(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


def paginate(query_total: int, items: list, params: PaginationParams) -> Paginated:
    return Paginated(items=items, total=query_total, page=params.page, page_size=params.page_size)
