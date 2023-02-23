from fastapi import FastAPI, Depends, Security, HTTPException, status
import secrets
from db import models
from db.schemas import User, Todo
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from utils.utility import get_api_key, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get('/users')
async def get_users(api_key: str = Security(get_api_key), db: Session = Depends(get_db)):
    return db.query(models.UserEntity).all()


@app.post('/api_key')
async def get_api_key(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(models.UserEntity).filter(models.UserEntity.email == user.email).first()
    if existing_user:
        return {'api_key': db.query(models.UserEntity).filter(models.UserEntity.email == user.email).first().api_key}

    new_user = models.UserEntity()
    new_user.email = user.email
    new_user.api_key = secrets.token_hex(64)

    db.add(new_user)
    db.commit()
    return {'api_key': new_user.api_key}
