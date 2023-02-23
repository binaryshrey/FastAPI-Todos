from fastapi import FastAPI, Depends
import secrets
from db import models
from db.schemas import User, Todo
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/')
# async def hello():
#     return {'message': 'Hello FastAPI'}


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
