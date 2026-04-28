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
python3 --version
```

### 3) Install uv (recommended) OR use pip

If you already use `uv`, keep using it. Otherwise you can install it:

```bash
python3 -m pip install -U uv
```

---

## Run the API locally (without Kong)

From this folder:

```bash
cd /Users/shreeharianbazhagan/Documents/UOB/apiassignment1-sound
uv sync
uv run uvicorn app.main:app --reload --port 3000
```

Open:
- Swagger UI: `http://localhost:3000/docs`
- OpenAPI JSON (generated): `http://localhost:3000/openapi.json`

### Basic Auth credentials (demo)

- username: `admin`
- password: `admin123`

---

## How to run + take screenshots (this is what your lecturer wants)

### Q1 + Q3 (run API directly)

```bash
cd /Users/shreeharianbazhagan/Documents/UOB/apiassignment1-sound
uv sync
uv run uvicorn app.main:app --reload --port 3000
```

Open Swagger UI and screenshot: `http://localhost:3000/docs`

Basic Auth demo creds:
- `admin / admin123`

Run these and screenshot the terminal outputs:

```bash
curl -i "http://localhost:3000/artists"                               # should be 401
curl -i -u admin:admin123 "http://localhost:3000/artists?offset=0&limit=2"  # 200
curl -i -u admin:admin123 -H "Content-Type: application/json" \
  -d '{"name":"NewArtist","genre":"Rock","albumsPublished":1,"username":"newartist"}' \
  "http://localhost:3000/artists"                                    # 201
curl -i -u admin:admin123 "http://localhost:3000/artists/NoSuchArtist"      # 404
```

Book service (screenshot REST/RPC/GraphQL all matching for id=1):

```bash
curl -s "http://localhost:3000/books/1" | python3 -m json.tool
curl -s -H "Content-Type: application/json" -d '{"id":1}' \
  "http://localhost:3000/getBook" | python3 -m json.tool
curl -s -H "Content-Type: application/json" \
  -d '{"query":"query { book(id: 1) { id title author } }"}' \
  "http://localhost:3000/graphql" | python3 -m json.tool
```

### Q2 (run through Kong and screenshot 429 + 413)

In a new terminal:

```bash
cd /Users/shreeharianbazhagan/Documents/UOB/apiassignment1-sound
docker compose up --build
```

Call through Kong (screenshot):

```bash
curl -i -u admin:admin123 "http://localhost:8000/artists?offset=0&limit=2"
```

Rate-limit screenshot (you should see 429 in the output):

```bash
for i in {1..30}; do curl -s -o /dev/null -w "%{http_code}\n" -u admin:admin123 "http://localhost:8000/artists"; done
```

Request-size-limit screenshot (you should see 413):

```bash
python3 - <<'PY'
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

### What to put in the ZIP + PDF

- **ZIP**: zip the whole `apiassignment1-sound/` folder (code + configs + spec)
- **PDF**: follow `docs/report-outline.md` and paste in:
  - Swagger UI screenshot
  - curl screenshots showing 200/201/401/404
  - Kong screenshots showing 429 and 413
  - REST vs RPC vs GraphQL screenshots for the same book
  - Comparison text from `docs/paradigms-comparison.md`

If you want, tell me what tool you’ll use to create the PDF (Word/Google Docs/LaTeX), and I’ll format the content into a clean “ready-to-paste” report layout for that tool.

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
curl -s "http://localhost:3000/books" | python3 -m json.tool
curl -s "http://localhost:3000/books/1" | python3 -m json.tool
```

RPC:

```bash
curl -s -H "Content-Type: application/json" -d '{"id":1}' \
  "http://localhost:3000/getBook" | python3 -m json.tool
```

GraphQL:

```bash
curl -s -H "Content-Type: application/json" \
  -d '{"query":"query { book(id: 1) { id title author } }"}' \
  "http://localhost:3000/graphql" | python3 -m json.tool
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
cd /Users/shreeharianbazhagan/Documents/UOB/apiassignment1-sound
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
python3 - <<'PY'
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

