
from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from fastapi.routing import APIRouter

from sqlalchemy.sql.functions import user
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash
from blog import hashing

router = APIRouter(
    prefix="/user",
    tags=['users']
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowUser])
def getAllUsers(db:Session = Depends(get_db)):
    blogs = db.query(models.User).all()
    return blogs

@router.get('/{id}', response_model=schemas.ShowUser)
def getUser(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user

@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    pass