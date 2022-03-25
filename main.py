
from fastapi import FastAPI

import models
from database import engine 
import Routers.userpost , Routers.users, Routers.Auth, Routers.Vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind= engine)

app = FastAPI()

# origins = ["https://www.google.com", "https://www.youtube.com/"]
# origins = ["*"]
origins = [
            "https://www.youtube.com",
             "https:www.google.com"
             ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") 
async def root():
    return {"message": "Welcome to FastApi"}

app.include_router(Routers.userpost.router)
app.include_router(Routers.users.router)
app.include_router(Routers.Auth.router)
app.include_router(Routers.Vote.router)
  

