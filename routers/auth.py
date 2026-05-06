from datetime import timedelta,datetime, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from config import settings
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi.templating import Jinja2Templates

router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context=CryptContext(schemes=['bcrypt'] , deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    phone_number:str=Field(min_length=10,max_length=10)

class Token(BaseModel):
    access_token:str
    token_type:str

    
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency=Annotated[Session,Depends(get_db)]

templates=Jinja2Templates(directory='templates')
##pages##
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

##Endpoints##
def authenticate_user(username:str,password:str, db):
    user=db.query(Users).filter(username == Users.username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user    

def create_access_token(username:str,user_id:int,role:str, expires_delta:timedelta):
    encode={'sub':username , 'id':user_id, 'role':role}
    expires= datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    

async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username:str=payload.get('sub')
            user_id:str=payload.get('id') 
            user_role:str = payload.get('role')
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User is not Validated!')
            return {'username':username,'id':user_id , 'role':user_role}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User is not Validated!')   
                
    
@router.post("/" , status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role="user",
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    
    db.add(create_user_model)
    db.commit()
    
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form_data.username , form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='User is not Validated!')
    token=create_access_token(user.username,user.id, user.role ,timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}
    




