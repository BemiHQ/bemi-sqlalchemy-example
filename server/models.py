from sqlalchemy import Column, Integer, String, Boolean, text

from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, nullable=False)
    task = Column(String, nullable=False)
    is_completed = Column(Boolean, server_default=None)
