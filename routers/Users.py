from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy import String
from sqlalchemy.orm import Session
from fastapi import APIRouter , Depends, HTTPException,Path
from starlette import status
from models import todos, Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext


router=APIRouter(
    prefix='/user',
    tags=['User']
    )
class user_verification(BaseModel):
    
    password:str
    new_password:str=Field(min_length=6)
    

def get_db():
    db=SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'] , deprecated='auto')

@router.get("/")
async def get_user_detail(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Exist")
    return db.query(Users).filter(Users.id==user.get('id')).first()


@router.put("/update_password")
async def update_pass(db:db_dependency,user:user_dependency,user_verification:user_verification):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed ")
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail="Error on password Change.")
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    

@router.put("/ph_no/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def update_ph(db:db_dependency,user:user_dependency , phone_number:str):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()
    