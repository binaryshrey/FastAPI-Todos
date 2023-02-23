from db.database import SessionLocal
from utils.constants import ADMIN_API_KEY
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi import Security, HTTPException, status

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(api_key_query: str = Security(api_key_query), api_key_header: str = Security(api_key_header)):
    if api_key_query in ADMIN_API_KEY:
        return api_key_query
    if api_key_header in ADMIN_API_KEY:
        return api_key_header

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
