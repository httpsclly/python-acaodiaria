from pydantic import BaseModel, EmailStr

class Task(BaseModel):
    id: int
    title: str
    description: str

class User(BaseModel):
    id: int
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True