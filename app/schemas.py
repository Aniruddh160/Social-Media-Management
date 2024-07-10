from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from typing import Literal



class ImageCreate(BaseModel):
    image_url: str
    

class ImageResponse(BaseModel):
    id: int
    image_url: str
   

    class Config:
        orm_mode = True
        from_attributes = True

class UserResponse(BaseModel):
    U_ID: int
    Email: EmailStr
    U_Created_AT: datetime
    followers_count: int  


class UserCreate(BaseModel):
    Email : EmailStr
    Password : str
    

    
    class Config:
        orm_mode = True 
        from_attributes = True
        
        
class TextsToneCreate(BaseModel):
    T_Title: str
    T_Content: str
    T_Published: bool = True
    images: List[ImageCreate] = []
    



class TextsToneResponse(BaseModel):
    T_ID: int
    T_Title: str
    T_Content: str
    T_Published: bool = True
    T_Created_AT: datetime
    Owner_id: int
    owner : UserResponse
    images: List[ImageResponse]

    class Config:
        orm_mode = True
        from_attributes : True
        

        
class UserLogin(BaseModel):
    Email : EmailStr
    Password : str
    
    class Config:
        orm_mode = True 
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type : str
    
    
class TokenData(BaseModel):
    id : Optional[str] = None

    

class VoteCreate(BaseModel):
    post_id : int
    dir : Literal[0, 1]
    
    class Config:
        orm_mode = True 
        from_attributes = True
        
        
class FollowCreate(BaseModel):
    followed_id: int

class FollowResponse(BaseModel):
    follower_id: int
    followed_id: int

    class Config:
        orm_mode = True
        from_attributes = True