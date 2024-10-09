from fastapi import FastAPI, HTTPException
from typing import List
from models import Task, User
from crud import TaskCRUD, UserCRUD
from schemas import TaskCreate, TaskUpdate, UserCreate, UserUpdate

app = FastAPI()

# Inicializa o CRUD de tarefas e usuários
task_crud = TaskCRUD()
user_crud = UserCRUD()

# Rotas de tarefas
@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    return task_crud.create_task(task)

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return task_crud.get_tasks()

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = task_crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    task = task_crud.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    success = task_crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# Rotas de usuários
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    return user_crud.create_user(user)

@app.get("/users/", response_model=List[User])
async def read_users():
    return user_crud.get_users()

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    user = user_crud.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    success = user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
