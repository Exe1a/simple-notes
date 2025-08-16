from fastapi import FastAPI

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Base, TasksModel, Task

app = FastAPI()
engine = create_engine("sqlite://", echo=True)

@app.get("/tasks")
async def print_tasks():
    with Session(engine) as session:
        return session.scalars(select(TasksModel)).all()

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int | None = None):
    with Session(engine) as session:
        return session.scalars(select(TasksModel).where(TasksModel.id == task_id)).all()

@app.post("/tasks")
async def make_task(task: Task | None = None):
    with Session(engine) as session:
        session.add(TasksModel(
            title = task.title,
            description = task.description,
            completed = task.completed))
        session.commit()
    return f"Задача '{task.title}' создана."

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int | None = None):
    pass

@app.post("/setup")
async def setup():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return "База Данных сброшена."