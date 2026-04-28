## BITS API Assignment 1 (Record Label + Kong + Paradigms)

This folder is a **self-contained** assignment workspace that implements:

- **Q1 (OpenAPI 3.1.1)**: Record Label “Artists API” (Basic Auth, pagination via `offset`/`limit`, `GET /artists`, `POST /artists`, `GET /artists/{artistname}`) + schemas
- **Q2 (Kong)**: rate limiting + request size limiting
- **Q3 (Paradigms)**: Book Info Service in **REST + RPC + GraphQL** returning the same data

You will generate **your own screenshots** while running the commands below, then paste them into your PDF.

---

## Prerequisites (install once)

### 1) Install Docker Desktop (for Kong)

Install and open Docker Desktop so it’s running.

### 2) Install Python 3.13 (already implied by your repo)

Check:

```bash
python --version
```

### 3) Install uv (recommended) OR use pip

If you already use `uv`, keep using it. Otherwise you can install it:

```bash
python -m pip install -U uv
```

---

## Run the API locally (without Kong)

From this folder:

```bash
cd  Users\Soundharya GP\OneDrive\Desktop\API Project\Assignment_1>
uv sync
uv run uvicorn app.main:app --reload --port 3000
```

Open:
- Swagger UI: `http://localhost:3000/docs`
- OpenAPI JSON (generated): `http://localhost:3000/openapi.json`

### Basic Auth credentials (demo)

- username: `admin`
- password: `admin123`

### Try the Artists endpoints (screenshots for Q1)

List artists (paginated):

```bash
curl -i -u admin:admin123 "http://localhost:3000/artists?offset=0&limit=2"
```

Create an artist:

```bash
curl -i -u admin:admin123 -H "Content-Type: application/json" \
  -d '{"name":"Adele","genre":"Pop","albumsPublished":4,"username":"adele"}' \
  "http://localhost:3000/artists"
```

Fetch by name:

```bash
curl -i -u admin:admin123 "http://localhost:3000/artists/Adele"
```

Unauthorized example:

```bash
curl -i "http://localhost:3000/artists"
```

### Try the Book service (screenshots for Q3)

REST:

```bash
curl -s "http://localhost:3000/books" | python -m json.tool
curl -s "http://localhost:3000/books/1" | python -m json.tool
```

RPC:

```bash
curl -s -H "Content-Type: application/json" -d '{"id":1}' \
  "http://localhost:3000/getBook" | python -m json.tool
```

GraphQL:

```bash
curl -s -H "Content-Type: application/json" \
  -d '{"query":"query { book(id: 1) { id title author } }"}' \
  "http://localhost:3000/graphql" | python -m json.tool
```

---

## OpenAPI 3.1.1 spec file (for Q1 submission)

Your hand-written spec is here:

- `openapi/record-label-openapi-3.1.1.yaml`

You can paste that into your PDF (and optionally show it in an editor screenshot).

---

## Run behind Kong (rate limit + request size limit) — Q2

Start the stack:

```bash
cd  Users\Soundharya GP\OneDrive\Desktop\API Project\Assignment_1>
docker compose up --build
```

Kong listens on:
- Proxy: `http://localhost:8000`
- Admin API: `http://localhost:8001` (for checking status only)

### Call the API through Kong

Artists via Kong (still requires Basic Auth):

```bash
curl -i -u admin:admin123 "http://localhost:8000/artists?offset=0&limit=2"
```

### Rate limit test (screenshot)

Run many requests quickly (you should eventually see `429 Too Many Requests`):

```bash
for i in {1..30}; do curl -s -o /dev/null -w "%{http_code}\n" -u admin:admin123 "http://localhost:8000/artists"; done
```

### Request size limit test (screenshot)

Send an oversized body (you should see a 413 error):

```bash
python - <<'PY'
import requests
big = {"name":"X"*200000,"genre":"Y","albumsPublished":1,"username":"u"}
r = requests.post("http://localhost:8000/artists", auth=("admin","admin123"), json=big)
print(r.status_code, r.text[:200])
PY
```

Stop:

```bash
docker compose down
```

---

## What to put in your PDF (minimum to score well)

- **Q1**: screenshot(s) of Swagger UI + curl showing `200`, `201`, `401`, `404`, and the OpenAPI YAML file.
- **Q2**: screenshot(s) of `429` (rate limiting) and `413` (request size limiting) via Kong.
- **Q3**:
  - screenshot(s) of REST response, RPC response, GraphQL response (all matching for the same book id)
  - a short comparison table (REST vs RPC vs GraphQL)

