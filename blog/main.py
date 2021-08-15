from fastapi import FastAPI

from . import models
from .database import  engine, get_db
from .routers import blog, user

app = FastAPI()

# Creates all db tables using engine 
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
