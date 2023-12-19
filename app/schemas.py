from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Users(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# what the response should look like
# so now the user gets to see only these details in the response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_true = True


class PostOut(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


# we can create the schemas for specific requests
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# # or modify for instead of updating all of them , we can create a class
# # that should only update published for instance
# class UpdatePost(BaseModel):
#     # title: str
#     # content: str
#     published: bool = True
