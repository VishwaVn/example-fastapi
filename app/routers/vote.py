from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter
from .. import schemas, database, model, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post of id {vote.post_id} does not exist.",
        )
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id
    )
    # print(vote.post_id, vote.dir)
    found_Vote = vote_query.first()
    # print(f"Is this query working {found_Vote}")
    if vote.dir == 1:
        if found_Vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added vote"}
    else:
        if not found_Vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
