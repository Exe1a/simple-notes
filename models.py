from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean

from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class TasksModel(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(300))
    completed: Mapped[bool] = mapped_column(Boolean)

class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False