from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import pymysql
import time
from .config import settings


mylist = [
    {"id": 1, "rating": 4, "title": "Some title", "content": "some content"},
    {"id": 2, "rating": 5, "title": "Some title 1", "content": "some content 1"},
]


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = False


def find_id(id):
    for posts in mylist:
        if posts["id"] == id:
            return posts


def find_index_id(id: int):
    for i, posts in enumerate(mylist):
        if posts["id"] == id:
            return i


while True:
    try:
        conn = pymysql.connect(
            host=settings.database_hostname,
            user=settings.database_username,
            password=settings.database_password,
            db=settings.database_name,
        )
        cursor = conn.cursor()
        print(f"Database was conntected successfully!!!")
        break
    except Exception as error:
        print(f"Connecting to the database Failed!!!")
        print(f"Error : {error}")
        time.sleep(2)  # sleep

app = FastAPI()


@app.get("/posts")
def get_posts():
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        print(f"This is posts cursor : {posts}")
        print(f"Type of the posts is : {type(posts)}")
    # return {"data" : "Get HttpRequest Works"}
    return {"Data": posts}


# @app.get("/posts")
# def get_posts():
#     with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#         cursor.execute("SELECT * FROM posts")
#         posts = cursor.fetchall()
#         # post_dict = posts.dict()
#         print(f"This is posts cursor : {posts}")
#         print(f"Type of the posts is : {type(posts)}")
#         print(" ")
#         for i in posts:
#             print(i)
#     return {"Data": posts}


###########################################################################
# @app.get("/posts/{id}")
# def get_post_id(id : int, response : Response):
#     new_post = find_id(id)
#     print(new_post)
#     if not new_post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"error": f"Post of id : {id} was not found."}
#     return {"got_id_data" : new_post}
# For the above Instead of using response.status code we can use the HTTPException which should be imported first

# @app.get("/posts/{id}")
# def get_post_id(id : int, response : Response):
#     new_post = find_id(id)
#     print(new_post)
#     if not new_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post of id : {id} was not found.")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"error": f"Post of id : {id} was not found."}
#     return {"got_id_data" : new_post}


@app.get("/posts/{id}")
def get_post_id(id: int, response: Response):
    # new_post = find_id(id)
    # print(new_post)
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = (%s)", (str(id)))
        new_post = cursor.fetchone()

        if not new_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post of id : {id} was not found.",
            )
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {"error": f"Post of id : {id} was not found."}
    return {"got_id_data": new_post}


##########################################################################
#######################################################################33
# @app.post("/posts")
# def create_post(post : Post):
#     post_dict = post.dict()
#     print(post_dict)
#     post_dict['id'] = randrange(0,10000)
#     mylist.append(post_dict)
#     print(mylist)
#     return {"Post_request" : post_dict}

# Whenever we create a new post the status code for the post should be of 201 created ok which does not so do the below

# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_post(post : Post):
#     post_dict = post.dict()
#     print(post_dict)
#     post_dict['id'] = randrange(0,10000)
#     mylist.append(post_dict)
#     print(mylist)
#     return {"Post_request" : post_dict}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            "INSERT INTO posts(title, content, published) VALUES(%s,%s,%s)",
            (post.title, post.content, post.published),
        )
        cursor.execute("SELECT * FROM posts WHERE id = LAST_INSERT_ID()")
        new_post = cursor.fetchone()
        conn.commit()
    return {"Post_request": new_post}


###########################################################################


# Creating delete request
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_id(id:int,):
#     delete_index = find_index_id(id)
#     print(delete_index)
#     if not delete_index:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Data at index {id} was not found.')
#     mylist.pop(delete_index)
#     print(mylist)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # return {"deleted_data" : f"Data Deleted at index {id}"}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_id(
    id: int,
):
    # delete_index = find_index_id(id)
    # print(delete_index)
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM posts WHERE id = (%s)", (str))
        deleted_post = cursor.fetchone()
        print(deleted_post)
        conn.commit()

        if not deleted_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Data at index {id} was not found.",
            )
        # mylist.pop(delete_i)
        # print(mylist)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"deleted_data" : f"Data Deleted at index {id}"}


@app.put("/posts/{id}")
def update_one(id: int, post: Post):
    post_dict = post.dict()
    index = find_index_id(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} was not found.",
        )
    post_dict["id"] = randrange(0, 10000)
    mylist[index] = post_dict
    print(mylist)
    return {"Put Data": post_dict}
