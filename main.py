from fastapi import FastAPI, Depends, Security, HTTPException, status
import uvicorn
import secrets
from db import models
from db.database import engine
from db.schemas import User, Todo
from sqlalchemy.orm import Session
from utils.utility import get_admin_api_key,get_users_api_key, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def welcome():
    return {'message': 'FastAPI TODO-App v1'}


@app.get('/users')
async def get_users(api_key: str = Security(get_admin_api_key), db: Session = Depends(get_db)):
    return db.query(models.UserEntity).all()


@app.delete('/users', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    db.query(models.UserEntity).filter(models.UserEntity.api_key == api_key).delete()
    db.commit()
    return {'message': 'user deleted!'}


@app.get('/todos')
async def get_todos(api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    user_id = db.query(models.UserEntity).filter(models.UserEntity.api_key == api_key).first().id
    return db.query(models.TodoEntity).filter(models.TodoEntity.owner_id == user_id).all()


@app.post('/todos', status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo, api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    if not todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request!")

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


@app.put('/todos', status_code=status.HTTP_202_ACCEPTED)
async def update_todo(todoID: int, todo: Todo, api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    if not todo or not todoID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request!")

    user_id = db.query(models.UserEntity).filter(models.UserEntity.api_key == api_key).first().id
    todo_to_update = db.query(models.TodoEntity).filter(models.TodoEntity.id == todoID).filter(models.TodoEntity.owner_id == user_id).first()

    if not todo_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!")

    todo_to_update.title = todo.title
    todo_to_update.description = todo.description
    todo_to_update.is_complete = todo.is_complete
    todo_to_update.priority = todo.priority
    db.add(todo_to_update)
    db.commit()
    return {'message': 'todo updated!'}


@app.delete('/todos', status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(todoID: int, api_key: str = Security(get_users_api_key), db: Session = Depends(get_db)):
    if not todoID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad request!")

    user_id = db.query(models.UserEntity).filter(models.UserEntity.api_key == api_key).first().id
    todo_to_delete = db.query(models.TodoEntity).filter(models.TodoEntity.id == todoID).filter(models.TodoEntity.owner_id == user_id).first()

    if not todo_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!")

    db.query(models.TodoEntity).filter(models.TodoEntity.id == todoID).filter(models.TodoEntity.owner_id == user_id).delete()
    db.commit()
    return {'message': 'todo deleted!'}


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
