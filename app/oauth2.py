from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.orm import Session
from .config import settings

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALORITHM = settings.algorithm
ACESSS_TOKEN_EXPIRE_MINTUES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACESSS_TOKEN_EXPIRE_MINTUES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALORITHM])
        id: Optional[str] = payload.get("user_id")
        print(f"From the verify acccess token method : {id}")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=int(id))
        # print(f"Printing token_data : {token_data}")
    except JWTError as e:
        print(f"THis is the error {e}")
        raise credentials_exception
    return token_data  ## returns this ,previously was not there/


# we can pass this a dependency, to any one of the path operation,
# take the token from the request automatically, extract the id,
# it's going to verify that the token is correct by calling the verify_access_token


def get_current_user(
    token: str = Depends(ouath2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user
