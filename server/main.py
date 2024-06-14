from bemi import Bemi, BemiFastAPIMiddleware
from typing import Union, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    BemiFastAPIMiddleware,
    set_context=lambda request : {
        "endpoint": request.url.path,
        "method": request.method,
        "user_id": 1,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todos", response_model = List[schemas.Todo])
def todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos

@app.post('/todos', status_code = status.HTTP_201_CREATED, response_model = schemas.Todo)
def todo_create(todo_attributes: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo = models.Todo(**todo_attributes.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.put("/todos/{id}/complete", response_model = schemas.Todo)
def todo_complete(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")

    todo.is_completed = not todo.is_completed
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{id}", status_code = status.HTTP_204_NO_CONTENT)
def todo_delete(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")

    db.delete(todo)
    db.commit()
