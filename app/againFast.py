from fastapi import FastAPI, status,Response, HTTPException
from pydantic import BaseModel
from random import randrange 

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = False 

mypost = [{"id":1, "rating":4,"title":"Some title","content":"some content"},
          {"id":2, "rating":5,"title":"Some title 1","content":"some content 1"}]

def find_post(id):
    for post in mypost:
        if post['id'] == id:
            return post 


def find_id_index(id:int):
    for i,post in enumerate(mypost):
        if post['id'] == id:
            return i

@app.get("/posts")
def get_posts():
    return {"data": mypost}

@app.get("/posts/{id}")
def get_id(id:int, response:Response):
    post = find_post(id)
    print(f"The pos form get_id : {post}")
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detial=f"Post with id {id} not found.")
    return {"get_id_data" : post}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    print(post_dict)
    mypost.append(post_dict)
    return {"data" : post_dict}


@app.delete("/posts/{id}")
def delete_post(id:int, status_code = status.HTTP_204_NO_CONTENT):
    index = find_id_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    mypost.pop(index)
    print(mypost)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_one(id:int, post:Post):
    index = find_id_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    mypost[index] = post_dict
    print(mypost)
    return {"data" : post_dict}