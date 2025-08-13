from fastapi import FastAPI
from pydantic import BaseModel
from random import randint

app = FastAPI()

tasks = dict()

def new_id() -> int:
    n_id = randint(1, 1000)
    while n_id in tasks.keys():
        n_id = randint(1, 1000)
    return n_id

class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

@app.get("/tasks")
async def print_tasks():
    return tasks.items()

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int | None = None):
    if task_id:
        if task_id in tasks.keys():
            return tasks[task_id]
        else:
            return "Задачи с таким ID не существует."
    else:
        return "Введите ID задачи."

@app.post("/tasks")
async def make_task(task: Task | None = None):
    if task:
        tasks.update({new_id(): task})
        return f"Задача добавлена."
    else:
        return "Запрос не содержит: title, description (optional), completed (optional)."

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int | None = None):
    if task_id:
        if task_id in tasks.keys():
            task = tasks.pop(task_id)
            return f'Задача {task_id} удалена.'
        else:
            return "Задачи с таким ID не существует."
    else:
        return "Введите ID задачи."