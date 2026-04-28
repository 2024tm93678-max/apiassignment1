from __future__ import annotations

from dataclasses import dataclass

from app.models import ArtistCreate, ArtistPublic, Book, BookCreate


@dataclass
class ArtistStore:
    _items: list[ArtistPublic]

    @classmethod
    def with_seed_data(cls) -> "ArtistStore":
        return cls(
            _items=[
                ArtistPublic(name="Radiohead", genre="Alternative", albumsPublished=9, username="radiohead"),
                ArtistPublic(name="Adele", genre="Pop", albumsPublished=4, username="adele"),
                ArtistPublic(name="Daft Punk", genre="Electronic", albumsPublished=4, username="daftpunk"),
            ]
        )

    def list(self, offset: int, limit: int) -> tuple[list[ArtistPublic], int]:
        total = len(self._items)
        return self._items[offset : offset + limit], total

    def create(self, payload: ArtistCreate) -> ArtistPublic:
        if self.get_by_name(payload.name) is not None:
            raise ValueError("Artist already exists")
        artist = ArtistPublic(**payload.model_dump())
        self._items.append(artist)
        return artist

    def get_by_name(self, name: str) -> ArtistPublic | None:
        for a in self._items:
            if a.name.lower() == name.lower():
                return a
        return None


@dataclass
class BookStore:
    _items: dict[int, Book]
    _next_id: int

    @classmethod
    def with_seed_data(cls) -> "BookStore":
        items = {
            1: Book(id=1, title="Clean Code", author="Robert C. Martin"),
            2: Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt, David Thomas"),
        }
        return cls(_items=items, _next_id=max(items) + 1)

    def list(self) -> list[Book]:
        return [self._items[k] for k in sorted(self._items)]

    def get(self, id: int) -> Book | None:
        return self._items.get(id)

    def create(self, payload: BookCreate) -> Book:
        new = Book(id=self._next_id, title=payload.title, author=payload.author)
        self._items[self._next_id] = new
        self._next_id += 1
        return new

