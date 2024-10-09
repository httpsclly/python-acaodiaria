from fastapi import FastAPI, HTTPException
from typing import List
from models import Task
from crud import TaskCRUD
from schemas import TaskCreate, TaskUpdate

app = FastAPI()

# Inicializa o CRUD de tarefas
task_crud = TaskCRUD()

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
