from pydantic import BaseModel, Field


class User(BaseModel):
    user_name: str = Field(min_length=1, max_length=20)
    email: str = Field(min_length=1, max_length=50)
    is_active: bool
    api_key: str


class Todo(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(lt=11, gt=-1)
    is_complete: bool
