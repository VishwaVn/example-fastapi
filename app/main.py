from fastapi import FastAPI, Depends
from random import randrange
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import model
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# from pydantic import BaseSettings

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(settings.database_password)


@app.get("/")
def root():
    return {"message": "Welcome fastapi!!"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# here is the test for sqlalchemy
# If we perform any kind of database operation with sqlalchemy within
# FastAPI, we want to make sure that we pass into our path operation
# function. So just call db
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    post = db.query(model.Post).all()
    return {"data": post}


########### LATEST ############################

# from fastapi import Response, status, HTTPException
# from fastapi.params import Body
# from typing import Optional, List
# from . import crud, models, schemas
# from .app import models
# from . import schemas, utils
# app = FastAPI()
# my_post = [
#     {
#         "title": "new title from the database",
#         "content": "Content from database",
#         "id": 1,
#     },
#     {
#         "title": "new title from the database 2",
#         "content": "Content from database 2",
#         "id": 2,
#     },
# ]

#####################################################################
# def find_post(id):
#     for post in my_post:
#         if post["id"] == id:
#             return post


# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p["id"] == id:
#             return i


# day 2
# anytime a post is send or we get a response properly from the api the status code should 201, but we get 202 response code
# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_post(post : Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0,10000)
#     my_post.append(post_dict)
#     return {"data" : post_dict}


# @app.post("/posts_new", status_code=status.HTTP_201_CREATED)
# def create_post(post:Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0,10000)
#     my_post.append(post_dict)
#     return {"data":post_dict}
# @app.get("/posts/{id}")
# def get_post(id):
# print(id)
# post = find_post(int(id))
# return {"post_detail" : f"Here is post {id}"}


# @app.get('/posts/{id}')
# def get_post(id : int, response : Response):
#     post = find_post(id)
#     # print(post)
#     if not post:
#         # response.status_code = 404
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id : {id} was not fount")
#         # instead of doing the below , do the above that does the same thing
#         # response.status_code = status.HTTP_404_NOT_FOUNDL
#         # return {'message' : f"Post with id : {id} was not fount"}
#     return {"post_detail" : post}


# @app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     index_delete = find_index_post(id)
#     if not index_delete:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"The post of id : {id} does not exist to delete")
#     my_post.pop(index_delete)
#     # Here writing the status code of 204 no content which is the code for deleting a data from the database
#     # but the return {'delete_post' : 'post was successfully deleted"} will be send a proof of deleted as we usually do
#     # return {"delete_post": "post was successfully deleted"}
#     # instead do the below using Response
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id : int, post: Post):
#     print(post)
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} does not exist.")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_post[index] = post_dict
#     return {"update_status" : post_dict}

# @app.put("/posts/{id}")
# def update_post(id : int, post: Post):
# with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#     cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
#                    (post.title, post.content, post.published, str(id)))
#     cursor.execute("SELECT * FROM posts WHERE id = LAST_INSERT_ID()")
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")


# return {"update_status" : updated_post}


# @app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     # index_delete = find_index_post(id)
#     with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#         cursor.execute("DELETE FROM posts WHERE id = (%s)",(str(id),))
#         deleted_post = cursor.fetchone()
#         print(deleted_post)
#         conn.commit()
#         if not deleted_post:
#             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"The post of id : {id} does not exist to delete")
#         # my_post.pop(index_delete)
#         # Here writing the status code of 204 no content which is the code for deleting a data from the database
#         # but the return {'delete_post' : 'post was successfully deleted"} will be send a proof of deleted as we usually do
#         # return {"delete_post": "post was successfully deleted"}
#         # instead do the below using Response
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_post[len(my_post)-1]
#     return {"latest" : post}


# @app.post("/createpost")
# def create_post(payload : dict = Body(...)):
#     print(payload)
# return {"newpost": f"title: {payload['title']} , content : {payload['content']}"}

# @app.post("/createposts")
# def create_post(payload : dict = Body(...)):
# print(payload)
# return {"new_post": f"title : {payload['title']}, content: {payload['content']} "}


# @app.post("/createposts")
# def create_post(new_post : Post):
#     # print(new_post)
#     # print(new_post.title)
#     # print(new_post.published)
#     # print(new_post.rating)
#     print(new_post)
#     print(new_post.dict())
#     return {"message" : new_post}

# class Post(BaseModel):
#     title : str
#     content: str
#     direction : bool = True
#     rate : Optional[int] = None


# @app.post("/posts")
# def create_posts(post: Post):
#     print(post)
#     print(post.dict())
#     return {"message" : post}
