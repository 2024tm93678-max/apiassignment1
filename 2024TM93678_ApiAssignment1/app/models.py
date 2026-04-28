from __future__ import annotations

from pydantic import BaseModel, Field


class ArtistBase(BaseModel):
    name: str = Field(min_length=1, examples=["Adele"])
    genre: str = Field(min_length=1, examples=["Pop"])
    albumsPublished: int = Field(ge=0, examples=[4])
    username: str = Field(min_length=1, examples=["adele"])


class ArtistCreate(ArtistBase):
    pass


class ArtistPublic(ArtistBase):
    pass


class ArtistPublicList(BaseModel):
    items: list[ArtistPublic]
    offset: int = Field(ge=0, examples=[0])
    limit: int = Field(ge=1, le=100, examples=[10])
    total: int = Field(ge=0, examples=[3])


class Book(BaseModel):
    id: int
    title: str
    author: str


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)

