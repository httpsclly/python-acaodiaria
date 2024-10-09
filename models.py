from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    description: str

class User(BaseModel):
    id: int
    username: str
    email: str
