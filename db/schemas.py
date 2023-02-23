from pydantic import BaseModel, Field


class User(BaseModel):
    email: str = Field(min_length=7, max_length=30, title='email ID')

    # Default config override
    class Config:
        schema_extra = {
            'example': {
                "email": "xyz@gmail.com",
            }
        }


class Todo(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(lt=11, gt=-1)
    is_complete: bool

    # Default config override
    class Config:
        schema_extra = {
            'example': {
                "title": "Buy Veggies",
                "description": "Potatoes, Tomatoes",
                "priority": 4,
                "is_complete": False,
            }
        }
