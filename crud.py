from typing import List
from models import Task
from schemas import TaskCreate, TaskUpdate

class TaskCRUD:
    def __init__(self):
        self.tasks = []
        self.counter = 1

    def create_task(self, task: TaskCreate) -> Task:
        new_task = Task(id=self.counter, **task.dict())
        self.tasks.append(new_task)
        self.counter += 1
        return new_task

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        if task:
            task.title = task_update.title or task.title
            task.description = task_update.description or task.description
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
