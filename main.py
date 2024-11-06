import mariadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Definindo as origens permitidas
origins = [
    "http://localhost:8100",  # Permitir o acesso da sua aplicação Ionic
    "http://127.0.0.1:8000",  # Adicione outras origens, se necessário
]

# Adicionando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Pode usar ["*"] para permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)



# Conexão com o banco de dados MariaDB
def get_db_connection():
    try:
        conn = mariadb.connect(
            user="root",      
            password="",    
            host="127.0.0.1",
            port=3306,
            database="task_manager"  
        )
        return conn
    except mariadb.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro no banco de dados.")

# Modelos de dados
class User(BaseModel):
    username: str
    email: str
    password: str

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    color: Optional[str] = None
    completed: bool = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    owner_id: int

# CRUD para Users
@app.post("/users/")
def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, user.password)
        )
        conn.commit()
        return {"message": "Usuário cadastrado com sucesso!"}
    except mariadb.Error as e:
        print(f"Erro ao inserir usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário.")
    finally:
        cursor.close()
        conn.close()

@app.get("/users/")
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        return [{"id": u[0], "username": u[1], "email": u[2]} for u in users]
    except mariadb.Error as e:
        print(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar usuários.")
    finally:
        cursor.close()
        conn.close()

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
            (user.username, user.email, user.password, user_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return {"message": "Usuário atualizado com sucesso!"}
    except mariadb.Error as e:
        print(f"Erro ao atualizar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário.")
    finally:
        cursor.close()
        conn.close()

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return {"message": "Usuário excluído com sucesso!"}
    except mariadb.Error as e:
        print(f"Erro ao excluir usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir usuário.")
    finally:
        cursor.close()
        conn.close()

# CRUD para Tasks
@app.post("/tasks/")
def create_task(task: Task):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO tasks (title, description, color, completed, start_time, end_time, owner_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (task.title, task.description, task.color, task.completed, task.start_time, task.end_time, task.owner_id)
        )
        conn.commit()
        return {"message": "Tarefa criada com sucesso!"}
    except mariadb.Error as e:
        print(f"Erro ao inserir tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar tarefa.")
    finally:
        cursor.close()
        conn.close()

@app.get("/tasks/")
def list_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, title, description, color, completed, start_time, end_time, owner_id FROM tasks")
        tasks = cursor.fetchall()
        return [{"id": t[0], "title": t[1], "description": t[2], "color": t[3], "completed": t[4], 
                 "start_time": t[5], "end_time": t[6], "owner_id": t[7]} for t in tasks]
    except mariadb.Error as e:
        print(f"Erro ao listar tarefas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar tarefas.")
    finally:
        cursor.close()
        conn.close()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """UPDATE tasks SET title = ?, description = ?, color = ?, completed = ?, start_time = ?, end_time = ?
               WHERE id = ?""",
            (task.title, task.description, task.color, task.completed, task.start_time, task.end_time, task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        return {"message": "Tarefa atualizada com sucesso!"}
    except mariadb.Error as e:
        print(f"Erro ao atualizar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar tarefa.")
    finally:
        cursor.close()
        conn.close()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        return {"message": "Tarefa excluída com sucesso!"}
    except mariadb.Error as e:
        print(f"Erro ao excluir tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir tarefa.")
    finally:
        cursor.close()
        conn.close()
