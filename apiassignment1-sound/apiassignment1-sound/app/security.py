from __future__ import annotations

import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic(auto_error=False)

_DEMO_USERS: dict[str, str] = {
    "admin": "admin123",
    "user": "user123",
}


def require_basic_auth(credentials: HTTPBasicCredentials | None = Depends(security)) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    expected = _DEMO_USERS.get(credentials.username)
    ok = expected is not None and secrets.compare_digest(credentials.password, expected)
    if not ok:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

