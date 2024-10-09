from typing import List
from models import Task, User
from schemas import TaskCreate, TaskUpdate, UserCreate, UserUpdate

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

class UserCRUD:
    def __init__(self):
        self.users = []
        self.counter = 1

    def create_user(self, user: UserCreate) -> User:
        new_user = User(id=self.counter, **user.dict())
        self.users.append(new_user)
        self.counter += 1
        return new_user

    def get_users(self) -> List[User]:
        return self.users

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_user(user_id)
        if user:
            user.username = user_update.username or user.username
            user.email = user_update.email or user.email
            return user
        return None

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if user:
            self.users.remove(user)
            return True
        return False
