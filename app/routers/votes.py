from multiprocessing import get_context
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from app.models import *
from app.database import *
from passlib.context import CryptContext
from app.schemas import *
from app.utils import hash_password
from app.oauth2 import *
import logging

# Initialize FastAPI
router3 = APIRouter(
    prefix="/vote",
    tags=['votes']
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router3.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.U_ID} is attempting to vote on post {vote.post_id} with direction {vote.dir}")
    
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.U_ID)
    found_vote = vote_query.first()
    
    if found_vote:
        logger.info(f"Found existing vote: {found_vote}")

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.U_ID} has already liked post {vote.post_id}")
        
        new_vote = Vote(user_id=current_user.U_ID, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        logger.info(f"User {current_user.U_ID} liked post {vote.post_id} successfully")
        return {"detail": "Post liked successfully"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.U_ID} has not liked post {vote.post_id}")
        
        vote_query.delete()
        db.commit()
        logger.info(f"User {current_user.U_ID} disliked post {vote.post_id} successfully")
        return {"detail": "Post disliked successfully"}
    