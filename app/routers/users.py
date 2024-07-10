from multiprocessing import get_context
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from app.models import *
from app.database import *
from passlib.context import CryptContext
from app.schemas import *
from app.utils import hash_password
from app.routers.auth import *
# Initialize FastAPI
router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.get("/view", status_code=status.HTTP_201_CREATED)
def get_users(db: Session = Depends(get_db)):
    rec_mess = db.query(User).all()
    return rec_mess

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def CreatUser(Users : UserCreate, db: Session = Depends(get_db)):
    
    Hashed_Password = hash_password(Users.Password)
    Users.Password  = Hashed_Password

    new_user = User(**Users.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return new_user
            
           
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def CreatUser(id : int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.U_ID == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    return user

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user