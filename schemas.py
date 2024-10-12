from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None

class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # Permite que o Pydantic converta os modelos ORM para dicionários

