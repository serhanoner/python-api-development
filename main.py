import fastapi
from fastapi import FastAPI, Response, status, exceptions
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', port=5433, database='fastapi',
                                user='postgres', password='postgres15-serhan',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(10)


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

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return id


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts",  status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""
    INSERT INTO posts (title, content, published) VALUES
    (%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    #have to commit the data into the database
    conn.commit()
    return {"data": new_post}
# title str, content str


# THE ORDER IS CRITICAL
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

# THE ORDER IS CRITICAL
@app.get("/posts/{id}")
def get_post(id:int,  response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", str(id))
    post = cursor.fetchone()
    if not post:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail=f"post with id: {id} not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #   return  {'message': f"post with id: {id} not found"}

    return {"post_detail": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index in the array that has the requested ID
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': "post_dict"}