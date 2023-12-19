from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi.params import Body


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True


app = FastAPI()

myposts = [
    {"title": "Title 1", "content": "content 1", "id": 1},
    {"title": "Title 2", "content": "content 2", "id": 2},
]


def find_post(id):
    for post in myposts:
        if post["id"] == id:
            return post


@app.get("/post")
def get_posts():
    return {"data": "got the posts"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    print(post_dict)
    myposts.append(post_dict)
    return {"post_data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = myposts[len(myposts) - 1]
    return {"latest_data": post}


@app.get("/posts/{id}")
def get_id(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} not found.",
        )
    return {"post_id_data": post}
