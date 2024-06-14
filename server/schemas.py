from typing import Union

from pydantic import BaseModel

class TodoBase(BaseModel):
    task: str

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    is_completed: Union[bool, None] = None
    class Config:
        orm_mode = True

