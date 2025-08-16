from fastapi import FastAPI

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Base, TasksModel, Task

app = FastAPI()
engine = create_engine("sqlite://", echo=True)

# Print all tasks
@app.get("/tasks")
async def print_tasks():
    with Session(engine) as session:
        return session.scalars(select(TasksModel)).all()

# Print task by ID
@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    with Session(engine) as session:
        return session.scalars(select(TasksModel).where(TasksModel.id == task_id)).all()

# Add task
@app.post("/tasks")
async def make_task(task: Task):
    with Session(engine) as session:
        session.add(TasksModel(
            title = task.title,
            description = task.description,
            completed = task.completed))
        session.commit()
    return f"Задача '{task.title}' создана."

# Delete task by ID
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    with Session(engine) as session:
        session.delete(session.get(TasksModel, task_id))
        session.commit()
    return f"Задача {task_id} удалена."

# Update completed status
@app.patch("/tasks/{task_id}")
async def update_task(
                    task_id: int,
                    status: bool):
    with Session(engine) as session:
        session.get(TasksModel, task_id).completed = status
        session.commit()
    return f"Статус задачи {task_id} изменен на {status}"

# Setup database
@app.post("/setup")
async def setup():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return "База Данных сброшена."