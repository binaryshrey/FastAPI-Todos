from fastapi import FastAPI
from db import models
from db.database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def hello():
    return {'message': 'Hello FastAPI'}
