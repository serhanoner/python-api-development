import fastapi
from fastapi import FastAPI, Response, status, exceptions
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [ {"title": "title of post 1",
              "content": "content of post 1",
              "id": 1},
             {"title": "favorite foods",
              "content": "I like pizza",
              "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",  status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# title str, content str


# THE ORDER IS CRITICAL
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

# THE ORDER IS CRITICAL
@app.get("/posts/{id}")
def get_post(id:int,  response: Response):

    post = find_post(id)
    if not post:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail=f"post with id: {id} not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #   return  {'message': f"post with id: {id} not found"}

    return {"post_detail": post}

