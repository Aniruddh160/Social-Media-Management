from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Follow, User
from app.schemas import FollowCreate, FollowResponse
from app.oauth2 import get_current_user

router4 = APIRouter(
    prefix="/follow",
    tags=['Follow']
)

@router4.post("/", status_code=status.HTTP_201_CREATED, response_model=FollowResponse)
def follow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if follow.followed_id == current_user.U_ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")

    follow_instance = db.query(Follow).filter(Follow.follower_id == current_user.U_ID, Follow.followed_id == follow.followed_id).first()
    
    if follow_instance:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are already following this user")
    
    new_follow = Follow(follower_id=current_user.U_ID, followed_id=follow.followed_id)
    db.add(new_follow)
    
    followed_user = db.query(User).filter(User.U_ID == follow.followed_id).first()
    followed_user.followers_count += 1
    
    db.commit()
    db.refresh(new_follow)
    
    return new_follow

@router4.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow_instance = db.query(Follow).filter(Follow.follower_id == current_user.U_ID, Follow.followed_id == follow.followed_id).first()
    
    if not follow_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following this user")
    
    followed_user = db.query(User).filter(User.U_ID == follow.followed_id).first()
    followed_user.followers_count -= 1
    
    db.delete(follow_instance)
    db.commit()
    
    return {"detail": "Unfollowed successfully"}
















# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models import Follow, User
# from app.schemas import FollowCreate, FollowResponse
# from app.oauth2 import get_current_user

# router4 = APIRouter(
#     prefix="/follow",
#     tags=['Follow']
# )

# @router4.post("/", status_code=status.HTTP_201_CREATED, response_model=FollowResponse)
# def follow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if follow.followed_id == current_user.U_ID:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")

#     follow_instance = db.query(Follow).filter(Follow.follower_id == current_user.U_ID, Follow.followed_id == follow.followed_id).first()
    
#     if follow_instance:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are already following this user")
    
#     new_follow = Follow(follower_id=current_user.U_ID, followed_id=follow.followed_id)
#     db.add(new_follow)
#     db.commit()
#     db.refresh(new_follow)
    
#     return new_follow

# @router4.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# def unfollow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     follow_instance = db.query(Follow).filter(Follow.follower_id == current_user.U_ID, Follow.followed_id == follow.followed_id).first()
    
#     if not follow_instance:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following this user")
    
#     db.delete(follow_instance)
#     db.commit()
#     print("Unfollowed Successfully")
#     return {"detail": "Unfollowed successfully"}
