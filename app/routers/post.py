from .. import model, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.sql.expression import func

router = APIRouter(prefix="/posts", tags=["Postshttp://127.0.0.1:8000/"])


#
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #     cursor.execute("SELECT * FROM posts")
    #     posts = cursor.fetchall()
    #     # post_dict = posts.dict()
    #     print(f"This is posts cursor : {posts}")
    #     print(f"Type of the posts is : {type(posts)}")
    #     print(" ")
    #     for i in posts:
    #         print(i)
    # posts = db.query(model.Post).all()
    print(limit)
    # posts = (
    #     db.query(model.Post)
    #     .filter(model.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True)
        .group_by(model.Post.id)
        .filter(model.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # serialized_results = [{"post": post[0], "votes": post[1]} for post in results]
    # print(serialized_results)
    # # print(results.dict())
    return posts


# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #     cursor.execute("SELECT * FROM posts WHERE id = (%s)", (str(id)))
    #     post = cursor.fetchone()
    #     print(post)
    #     # post = find_post(id)
    #     if not post:
    #         # response.status_code = 404
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Post with id : {id} was not fount",
    #         )
    # post = db.query(model.Post).filter(model.Post.id == id).first()

    post = (
        db.query(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True)
        .group_by(model.Post.id)
        .filter(model.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist.",
        )
        # instead of doing the below , do the above that does the same thing
        # response.status_code = status.HTTP_404_NOT_FOUNDL
        # return {'message' : f"Post with id : {id} was not fount"}
    return post


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_post[len(my_post) - 1]
#     return {"latest": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # index_delete = find_index_post(id)
    # with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #     cursor.execute("DELETE FROM posts WHERE id = (%s)", (str(id),))
    #     deleted_post = cursor.fetchone()
    #     print(deleted_post)
    #     conn.commit()
    #     if not deleted_post:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"The post of id : {id} does not exist to delete",
    #         )
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist.",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized  to perform requested action.",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_post.pop(index_delete)
    # Here writing the status code of 204 no content which is the code for deleting a data from the database
    # but the return {'delete_post' : 'post was successfully deleted"} will be send a proof of deleted as we usually do
    # return {"delete_post": "post was successfully deleted"}
    # instead do the below using Response

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #     # cursor.execute("INSERT INTO posts(title, content, published) VALUES(%s,%s,%s)",(post.title, post.content, post.published))
    #     # conn.commit()
    #     cursor.execute(
    #         "INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)",
    #         (post.title, post.content, post.published),
    #     )
    #     # Commit the changes to the database

    #     # Retrieve the newly inserted post by its ID
    #     cursor.execute("SELECT * FROM posts WHERE id = LAST_INSERT_ID()")
    #     new_post = cursor.fetchone()
    #     conn.commit()
    #     # new_post = cursor.fetchone()
    #     print(new_post)
    # new_post = model.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    print(f"From the posts endpoint{current_user.email}")
    print(type(current_user.email))
    new_post = model.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put(
    "/{id}", response_model=schemas.Post
)  # we have to change the post:Post post name to something else here I will change it to updated_post, previouslt it was updated post
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):  # because using the sqlalchemy also I am using post to fetch the data so it overlaps and will create error
    # with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #     cursor.execute(
    #         "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
    #         (post.title, post.content, post.published, str(id)),
    #     )
    #     conn.commit()

    # with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    #     cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    #     updated_post = cursor.fetchone()
    #     if updated_post == None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"Post with id {id} not found.",
    #         )
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found.",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized  to perform requested action.",
        )

    print(f"Updated post outside the with : {updated_post}, id : {id}")
    # if updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} does not exist.")
    # post.update(
    #     {"title": "Updated_title", "content": "Updated content"},
    #     synchronize_session=False,
    # )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
