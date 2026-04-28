from __future__ import annotations

import strawberry

from app.models import Book
from app.storage import BookStore


@strawberry.type
class BookType:
    id: int
    title: str
    author: str


def build_schema(book_store: BookStore) -> strawberry.Schema:
    @strawberry.type
    class Query:
        @strawberry.field
        def book(self, id: int) -> BookType | None:
            b: Book | None = book_store.get(id)
            if b is None:
                return None
            return BookType(id=b.id, title=b.title, author=b.author)

    return strawberry.Schema(query=Query)

