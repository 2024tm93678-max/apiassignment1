## REST vs RPC vs GraphQL (Book Info Service)

### REST (Representational State Transfer)
- **How you call it**: multiple endpoints (resources) like `GET /books/1`
- **Data shape**: server-defined (fixed response per endpoint)
- **Pros**: simple, cache-friendly, maps well to HTTP status codes, widely used
- **Cons**: can cause under/over-fetching (you might get more fields than you need)

### RPC (Remote Procedure Call)
- **How you call it**: “function-like” endpoints like `POST /getBook` with JSON body `{"id":1}`
- **Data shape**: often server-defined; not resource-oriented
- **Pros**: feels like calling methods, easy to model actions/commands
- **Cons**: less standard HTTP semantics, can become a large “API methods” list

### GraphQL
- **How you call it**: single endpoint (commonly) like `POST /graphql` with a query
- **Data shape**: client-defined (client asks exactly which fields)
- **Pros**: avoids over/under-fetching; strong typing; flexible queries
- **Cons**: more tooling/complexity; caching is more complex than REST

### Evidence in this project
All three styles return identical “book” data for the same id:
- REST: `GET /books/1`
- RPC: `POST /getBook` with `{"id":1}`
- GraphQL: `query { book(id: 1) { id title author } }`

