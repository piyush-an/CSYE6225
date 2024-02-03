import os
import time
from fastapi import FastAPI, Request
from dotenv import load_dotenv
load_dotenv() 
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
security = HTTPBasic()
app = FastAPI()

def fake_hash_password(password: str):
    # return "fakehashed" + password
    return password + "notreallyhashed"

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verification(creds: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, username=creds.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username is not registered")
    else:
        # print(f"db_user.hashed_password ======== {db_user.hashed_password} \n creds.password ======== {fake_hash_password(creds.password)}")
        if fake_hash_password(creds.password) != db_user.hashed_password:
            raise HTTPException(status_code=400, detail="Password is incorrect")
        else:
            print(f"User is authenticated")
            return db_user


@app.get("/v1/user/self", response_model=schemas.User, tags=["authenticated"])
def read_users(Verifcation = Depends(verification), db: Session = Depends(get_db)):
    if Verifcation:
        return Verifcation
    
@app.put("/v1/user/self2", response_model=schemas.User, tags=["authenticated"])
def read_users(Verifcation = Depends(verification), user: schemas.UserCreate, db: Session = Depends(get_db)):
    if Verifcation:
        return Verifcation


# @app.get("/")
# async def root():
#     return {"message": "CSYE 6225 - Spring 2024"}


@app.get("/healthz", tags=["public"])
async def healthz():
    return {"message": "OK"}


@app.post("/v1/user", response_model=schemas.User, tags=["public"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/v1/user/all", response_model=list[schemas.User], tags=["public"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users



