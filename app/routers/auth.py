from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, model, utils, oauth2

router = APIRouter(tags=["Authentication"])


# user_credentials: schemas.UserLogin
@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OauthpasswordRequestform returnxs the below
    # {
    #     "username":"adadad",
    #     "password": "paswdda"
    # } user_credentials.email
    user = (
        db.query(model.User)
        .filter(model.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # Create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return {"token": "example token"}
    return {"access_token": access_token, "token_type": "bearer"}
