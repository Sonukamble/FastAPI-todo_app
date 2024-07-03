from typing import Annotated

import models as models
from database import SessionLocal, engine
from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@admin_router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Todos).all()


@admin_router.delete("/delete/{todo_id}")
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(get=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
