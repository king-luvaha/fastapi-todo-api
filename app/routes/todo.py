from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, auth
from app.dependencies import get_db

router = APIRouter(tags=["Todos"])


# -------- CREATE -------- #
@router.post("/todos/", response_model=schemas.TodoOut)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_todo = models.Todo(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo