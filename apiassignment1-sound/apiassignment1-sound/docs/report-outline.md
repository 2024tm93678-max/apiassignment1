## PDF Report Outline (copy/paste and add screenshots)

### 1) OpenAPI 3.1.1 Specification (Record Label / Artists) — 10 marks
- **Spec file**: `openapi/record-label-openapi-3.1.1.yaml`
- **Security**: Basic Auth (`components.securitySchemes.basicAuth`)
- **Endpoints**
  - `GET /artists` with pagination: `offset`, `limit`
  - `POST /artists` create artist
  - `GET /artists/{artistname}` fetch by artist name
- **Screenshots to include**
  - Swagger UI showing the `Artists` endpoints
  - Terminal calls showing:
    - `200 OK` (authorized list)
    - `201 Created` (create artist)
    - `401 Unauthorized` (missing/invalid credentials)
    - `404 Not Found` (unknown artist name)

### 2) Kong API Gateway Limits — 6 marks
- **Config**: `kong/kong.yaml` (declarative config, DB-less)
- **Enabled plugins**
  - `rate-limiting`
  - `request-size-limiting`
- **Screenshots to include**
  - A burst of requests showing `429 Too Many Requests`
  - Oversized POST body showing `413 Request size limit exceeded`

### 3) Book Info Service: REST vs RPC vs GraphQL — 9 marks
- **REST**
  - `GET /books`
  - `GET /books/{id}`
- **RPC**
  - `POST /getBook`
  - `POST /createBook`
- **GraphQL**
  - `POST /graphql` with `query { book(id: 1) { title author } }`
- **Screenshots to include**
  - REST response for id=1
  - RPC response for id=1
  - GraphQL response for id=1
  - (Optional) screenshot of GraphQL Playground if you open it in browser
- **Comparison section**
  - Use `docs/paradigms-comparison.md` as your comparison text

