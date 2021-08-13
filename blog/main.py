from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas, models
from .database import  SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash
from blog import hashing

app = FastAPI()

# Creates all db tables using engine 
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/blog', response_model=List[schemas.ShowBlog])
def getAllBlogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def getBlog(id, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.update({'title':request.title, 'body':request.body})
    db.commit()
    return 'updated'

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail':'done'}


@app.get('/user', response_model=List[schemas.ShowUser])
def getAllUsers(db:Session = Depends(get_db)):
    blogs = db.query(models.User).all()
    return blogs

@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.passwordk))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    pass