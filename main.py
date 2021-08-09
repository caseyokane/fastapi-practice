from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index(limit=10, published:Optional[bool]=False, sort:Optional[str]=None):
    if published:
        return {'data': f'{limit} blogs from list' }
    else:
        return {'data': '0 blogs from list' }

@app.get('/about')
def about():
    return {'data': 'about page'}

# Put static route before dynamic 
@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs' }

@app.get('/blog/{id}')
def show(id:int):
    return {'data': id }

@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    return limit

class Blog(BaseModel):
    title: str
    body: str 
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f"Blog is created as {blog.title}"}