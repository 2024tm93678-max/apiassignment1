from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from strawberry.fastapi import GraphQLRouter

from app.models import ArtistCreate, ArtistPublic, ArtistPublicList, Book, BookCreate
from app.security import require_basic_auth
from app.storage import ArtistStore, BookStore

security = HTTPBasic(auto_error=False)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Record Label API + Book Info Service",
        version="1.0.0",
        summary="Assignment demo: OpenAPI + REST/RPC/GraphQL + Kong limits",
    )

    artist_store = ArtistStore.with_seed_data()
    book_store = BookStore.with_seed_data()

    # --------------------------
    # Q1: Record Label Artists API
    # --------------------------
    @app.get(
        "/artists",
        response_model=ArtistPublicList,
        dependencies=[Depends(require_basic_auth)],
        tags=["Artists"],
        summary="List artists (paginated)",
    )
    def list_artists(
        offset: int = Query(0, ge=0, description="Page offset (0-based)"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
    ) -> ArtistPublicList:
        items, total = artist_store.list(offset=offset, limit=limit)
        return ArtistPublicList(items=items, offset=offset, limit=limit, total=total)

    @app.post(
        "/artists",
        response_model=ArtistPublic,
        status_code=201,
        dependencies=[Depends(require_basic_auth)],
        tags=["Artists"],
        summary="Create a new artist",
    )
    def create_artist(payload: ArtistCreate) -> ArtistPublic:
        try:
            return artist_store.create(payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @app.get(
        "/artists/{artistname}",
        response_model=ArtistPublic,
        dependencies=[Depends(require_basic_auth)],
        tags=["Artists"],
        summary="Get artist by name",
    )
    def get_artist_by_name(artistname: str) -> ArtistPublic:
        artist = artist_store.get_by_name(artistname)
        if artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return artist

    # --------------------------
    # Q3: Book Info Service (REST)
    # --------------------------
    @app.get("/books", response_model=list[Book], tags=["Books (REST)"], summary="List books")
    def list_books() -> list[Book]:
        return book_store.list()

    @app.get(
        "/books/{id}",
        response_model=Book,
        tags=["Books (REST)"],
        summary="Get book by id",
    )
    def get_book(id: int) -> Book:
        book = book_store.get(id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    @app.post(
        "/books",
        response_model=Book,
        status_code=201,
        tags=["Books (REST)"],
        summary="Create book",
    )
    def create_book(payload: BookCreate) -> Book:
        try:
            return book_store.create(payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    # --------------------------
    # Q3: Book Info Service (RPC style)
    # --------------------------
    @app.post("/getBook", response_model=Book, tags=["Books (RPC)"], summary="RPC getBook")
    def rpc_get_book(body: dict) -> Book:
        raw_id = body.get("id")
        if raw_id is None:
            raise HTTPException(status_code=400, detail="Missing field: id")
        if not isinstance(raw_id, int):
            raise HTTPException(status_code=400, detail="Field id must be an integer")
        book = book_store.get(raw_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    @app.post(
        "/createBook",
        response_model=Book,
        status_code=201,
        tags=["Books (RPC)"],
        summary="RPC createBook",
    )
    def rpc_create_book(body: dict) -> Book:
        title = body.get("title")
        author = body.get("author")
        if not isinstance(title, str) or not title.strip():
            raise HTTPException(status_code=400, detail="title is required")
        if not isinstance(author, str) or not author.strip():
            raise HTTPException(status_code=400, detail="author is required")
        try:
            return book_store.create(BookCreate(title=title, author=author))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    # --------------------------
    # Q3: Book Info Service (GraphQL)
    # --------------------------
    from app.schema import build_schema

    schema = build_schema(book_store=book_store)
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql", tags=["Books (GraphQL)"])

    # --------------------------
    # Small helper endpoint (useful for Kong health checks)
    # --------------------------
    @app.get("/health", tags=["Health"])
    def health() -> dict:
        return {"ok": True}

    return app


app = create_app()

