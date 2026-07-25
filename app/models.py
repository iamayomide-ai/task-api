from sqlalchemy import Column, String, Boolean
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)
