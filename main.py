from fastapi import FastAPI

import models
from database import engine
from router.auth import router
from router.todos import todo_router
from router.admin import admin_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(todo_router)
app.include_router(admin_router)
