
from fastapi import FastAPI
from config import setting

import models
from database import engine 
import Routers.userpost , Routers.users, Routers.Auth, Routers.Vote


models.Base.metadata.create_all(bind= engine)

app = FastAPI()


@app.get("/") 
async def root():
    return {"message": "Welcome to FastApi"}

app.include_router(Routers.userpost.router)
app.include_router(Routers.users.router)
app.include_router(Routers.Auth.router)
app.include_router(Routers.Vote.router)
  

