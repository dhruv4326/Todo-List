from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI , Depends, HTTPException,Path
from starlette import status
import models
from models import todos
from database import engine, Session_local

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=Session_local()
    
    try:
        yield db
    finally:
        db.close()
 
db_dependency=Annotated[Session,Depends(get_db)]

# BaseModel Creation
class TodoRequest(BaseModel):
    title:str = Field(max_length=100,min_length=1)
    description:str=Field(max_length=300)
    priority:int = Field(gt=0,lt=6)
    Complete:bool 
    
    
            
@app.get("/",status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db:db_dependency,todo_id:int=Path(gt=0)):
    todo_model= db.query(todos).filter(todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404 , detail='There is no task entered for this id.')   
    
    
@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,todo_request:TodoRequest):
    todo_model= todos(**todo_request.model_dump())
    
    db.add(todo_model)
    db.commit()
    
    
    
@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,todo_request:TodoRequest, todo_id:int=Path(gt=0)):
    todo_model= db.query(todos).filter(todos.id==todo_id).first()
    if todo_model is not None:
        todo_model.title= todo_request.title
        todo_model.description=todo_request.description
        todo_model.priority=todo_request.priority
        todo_model.Complete=todo_request.Complete
        
        db.add(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404,detail="Item not found!!")
        

@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(db:db_dependency,todo_id:int=Path(gt=0)):
    todo_model=db.query(todos).filter(todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo task you want to delete is not exists!')
    db.query(todos).filter(todos.id==todo_id).delete()
    
    db.commit()