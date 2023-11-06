import fastapi
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(payload: dict = fastapi.Body()):
    print(payload)
    return {"data": f"title {payload['title']}, content: {payload['content']}"}
# title str, content str

