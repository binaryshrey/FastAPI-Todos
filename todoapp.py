from fastapi import FastAPI, Depends, Security, HTTPException, status
import secrets
from db import models
from db.schemas import User, Todo
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from utils.utility import get_admin_api_key,get_users_api_key, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get('/users')
async def get_users(api_key: str = Security(get_admin_api_key), db: Session = Depends(get_db)):
    return db.query(models.UserEntity).all()


@app.get('/todos')
async def get_todos(api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    user_id = db.query(models.UserEntity).filter(models.UserEntity.api_key == api_key).first().id
    return db.query(models.TodoEntity).filter(models.TodoEntity.owner_id == user_id).all()


@app.post('/todos', status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo, api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    user_id = db.query(models.UserEntity).filter(models.UserEntity.api_key == api_key).first().id
    new_todo = models.TodoEntity()
    new_todo.title = todo.title
    new_todo.description = todo.description
    new_todo.is_complete = todo.is_complete
    new_todo.priority = todo.priority
    new_todo.owner_id = user_id
    db.add(new_todo)
    db.commit()
    return {'message': 'new todo added!'}


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
