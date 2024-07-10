from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import *
from app.models import *
from app.utils import *
from app.oauth2 import *
from app.send_email import send_login_notification
from app.routers.follow import *


router2 = APIRouter(
    tags=['Authentication']
)

@router2.post('/login', response_model= Token)
def login(user_credential : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.Email == user_credential.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Creds")
    
    if verify_password(user_credential.password, user.Password) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    
    access_token = create_access_token(data = {"user_id" : user.U_ID})
    
    # Send login notification email
    send_login_notification(user.Email)
    print("Email sent")
    
    return {"access_token": access_token, "token_type": "bearer"}


# @router2.post("/login")
# def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.Email == user_credential.username).first()
#     if not user or not verify_password(user_credential.password, user.Password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     access_token = create_access_token(data = {"user_id" : user.U_ID})
#     send_login_notification(user.Email)
#     print("Email sent")
#     return {"access_token": access_token, "token_type": "bearer", "followers_count": User.followers_count}