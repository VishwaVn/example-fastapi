from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(
        String(255), nullable=False
    )  # wrote String not String(255) so got an error
    content = Column(String(255), nullable=False)
    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # if u want to get all the information of the user given that it has a foriegn key or some kind of relationship, then we can get all the information of the user
    # that this post is associated with
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    phone_number = Column(String(255))


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String(255), nullable=False)
#     content = Column(String(255), nullable=False)
#     published = Column(Boolean, server_default=text("TRUE"), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
# created_at = Column(
#     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
# )
# published = Column(Boolean,  default=True)
