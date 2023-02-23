from db import models
from sqlalchemy.orm import Session
from db.database import SessionLocal
from utils.constants import ADMIN_API_KEY
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi import Security, HTTPException, status, Depends

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_admin_api_key(query_key: str = Security(api_key_query),
                      header_key: str = Security(api_key_header)):
    if query_key in ADMIN_API_KEY:
        return query_key
    if header_key in ADMIN_API_KEY:
        return header_key

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")


def get_users_api_key(query_key: str = Security(api_key_query),
                      header_key: str = Security(api_key_header),
                      db: Session = Depends(get_db)):
    API_KEYS = [user.api_key for user in db.query(models.UserEntity)]

    if query_key in API_KEYS:
        return query_key
    if header_key in API_KEYS:
        return header_key

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")