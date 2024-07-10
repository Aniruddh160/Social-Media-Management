#importing necessary modules required for API calls
from ..import simple
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from app.models import TextsTone, User
from app.database import *
from typing import List
from app.schemas import TextsToneCreate, TextsToneResponse
from app.oauth2 import *
from app.utils import *
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os   
import shutil
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.orm import joinedload

# Initialize FastAPI
router1 = APIRouter(
    prefix="/messages",
    tags=['Posts']
)




'''
This API is the home page or the page that the user will see when they first visit the site.
'''
@router1.get("/")
def hello_world():
   return {"data": "Hello World"}



''' This API is for the user to view all the messages that have been posted on the site '''
@router1.get("/view", response_model=List[TextsToneResponse])
def get_messages(db: Session = Depends(get_db), id : int = Depends(get_current_user)):
    rec_mess = db.query(TextsTone).all()
    for message in rec_mess:
        if message.T_Published is None:
            message.T_Published = True  # Or handle appropriately
    
    return rec_mess

# @router1.get("/view", response_model=List[TextsToneResponse])
# def get_messages(db: Session = Depends(get_db)):
#     rec_mess = db.query(TextsTone).options(joinedload(TextsTone.images)).all()
#     print("Fetched messages from DB:", rec_mess)  # Debug print
#     response = [TextsToneResponse.from_orm(mess) for mess in rec_mess]
#     print("Response after conversion:", response)  # Debug print
#     return response


'''This API is for the user to view all the messages that have been posted by a particular user '''
@router1.get("/view/posts", response_model=List[TextsToneResponse])
def get_messages(db: Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    rec_mess = db.query(TextsTone).filter(TextsTone.Owner_id == current_user.U_ID).all()
    for message in rec_mess:
        if message.T_Published is None:
            message.T_Published = True  # Or handle appropriately
    print(rec_mess)
    return rec_mess


'''
#This is code that has been commented because this code was used for a feature/function that has been updated.

# @router1.post("/", status_code=status.HTTP_201_CREATED, response_model=TextsToneResponse)
# def create_messages(
#     texts_tone: TextsToneCreate, 
#     db: Session = Depends(get_db), 
#     current_u: User = Depends(get_current_user)
# ):
    
#     new_message = TextsTone()
    
#     if current_u is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not authenticated"
#         )

#     attributes = {
#         "T_Title": texts_tone.T_Title,
#         "T_Content": texts_tone.T_Content,
#         "T_Published": texts_tone.T_Published,
#         "Owner_id": current_u.U_ID
#     } 
#     for key, value in attributes.items():
#         setattr(new_message, key, value)
        
        
#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)
#     return new_message


# @router1.post("/", status_code=status.HTTP_201_CREATED, response_model=TextsToneResponse)
# def create_messages(
#     texts_tone: TextsToneCreate,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(get_current_user)
    
# ):
#     print(f"Verifying content: Title: {texts_tone.T_Title}, Content: {texts_tone.T_Content}")  # Debug print

#     # Verify the content of the post
#     if not verify_content(texts_tone.T_Title, texts_tone.T_Content):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="The content contains harmful material and cannot be posted."
#         )

#     # Create a new message instance
#     new_message = TextsTone(
#         T_Title=texts_tone.T_Title,
#         T_Content=texts_tone.T_Content,
#         T_Published=texts_tone.T_Published,
#         Owner_id=current_user.U_ID  # Assuming current_user is an instance of User with U_ID attribute
#     )
    
#     # Add to the database session
#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)
    
#     for image in texts_tone.images:
#         new_image = Posts_image(post_id=new_message.T_ID, image_url=image.image_url)
#         db.add(new_image)
#         db.commit()
#         db.refresh(new_image)
#         new_message.images.append(new_image)
        
        
#     return new_message
'''

''' This API is for the user to create a new post. This APi bears a function that checks the content of the post to ensure that it does not contain any harmful material.
 This Function is called verify_content(), The function is integrated with a 3rd party API (Gemini Google) which reads through content posted by a particular user and 
brands it as 'harmful'/'not harmful' content.'''

UPLOAD_DIRECTORY = "images/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router1.post("/", status_code=status.HTTP_201_CREATED, response_model=TextsToneResponse)
def create_messages(
    T_Title: str = Form(...),
    T_Content: str = Form(...),
    T_Published: bool = Form(True),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"Verifying content: Title: {T_Title}, Content: {T_Content}")  # Debug print

    # Verify the content of the post
    if not verify_content(T_Title, T_Content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The content contains harmful material and cannot be posted."
        )

    # Create a new message instance
    new_message = TextsTone(
        T_Title=T_Title,
        T_Content=T_Content,
        T_Published=T_Published,
        Owner_id=current_user.U_ID  # Assuming current_user is an instance of User with U_ID attribute
    )
    
    # Add to the database session
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    # Handle file uploads and store image paths in the database
    for file in files:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        print(f"Saving file to: {file_location}")
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        image_url = f"/{UPLOAD_DIRECTORY}{file.filename}"
        new_image = Posts_image(post_id=new_message.T_ID, image_url=image_url)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        new_message.images.append(new_image)
        
    return new_message

# @router1.post("/", status_code=status.HTTP_201_CREATED, response_model=TextsToneResponse)
# def create_messages(
#     T_Title: str = Form(...),
#     T_Content: str = Form(...),
#     T_Published: bool = Form(True),
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     print(f"Verifying content: Title: {T_Title}, Content: {T_Content}")  # Debug print

#     # Verify the content of the post
#     if not verify_content(T_Title, T_Content):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="The content contains harmful material and cannot be posted."
#         )

#     try:
#         # Create a new message instance
#         new_message = TextsTone(
#             T_Title=T_Title,
#             T_Content=T_Content,
#             T_Published=T_Published,
#             Owner_id=current_user.U_ID  # Assuming current_user is an instance of User with U_ID attribute
#         )

#         # Add to the database session
#         db.add(new_message)
#         db.commit()
#         db.refresh(new_message)
        
#         # Handle file uploads and store image data in the database
#         for file in files:
#             image_data = file.file.read()
#             # Provide a default or placeholder value for image_url
#             new_image = Posts_image(
#                 post_id=new_message.T_ID,
#                 image_url="default_image_url",  # Provide a default image URL
#                 image_data=image_data  # Ensure image_data is binary
#             )
#             db.add(new_image)
#             db.commit()
#             db.refresh(new_image)
#             new_message.images.append(new_image)

#         # Commit the changes to ensure all images are added
#         db.commit()
#         db.refresh(new_message)

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")

#     return new_message

@router1.post("/", status_code=status.HTTP_201_CREATED, response_model=TextsToneResponse)
def create_messages(
    T_Title: str = Form(...),
    T_Content: str = Form(...),
    T_Published: bool = Form(True),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"Verifying content: Title: {T_Title}, Content: {T_Content}")  # Debug print

    # Verify the content of the post
    if not verify_content(T_Title, T_Content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The content contains harmful material and cannot be posted."
        )

    try:
        # Create a new message instance
        new_message = TextsTone(
            T_Title=T_Title,
            T_Content=T_Content,
            T_Published=T_Published,
            Owner_id=current_user.U_ID  # Assuming current_user is an instance of User with U_ID attribute
        )

        # Add to the database session
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        
        # Handle file uploads and store image data in the database
        for file in files:
            image_data = file.file.read()
            # Provide a default or placeholder value for image_url
            new_image = Posts_image(
                post_id=new_message.T_ID,
                image_url="default_image_url",  # Provide a default image URL
                image_data=image_data  # Ensure image_data is binary
            )
            db.add(new_image)
            db.commit()
            db.refresh(new_image)
            new_message.images.append(new_image)

        # Commit the changes to ensure all images are added
        db.commit()
        db.refresh(new_message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")

    return new_message


# @router1.get("/images/{image_id}")
# def get_image(image_id: int, db: Session = Depends(get_db)):
#     image = db.query(Posts_image).filter(Posts_image.id == image_id).first()
#     if not image:
#         raise HTTPException(status_code=404, detail="Image not found")
    
#     return StreamingResponse(io.BytesIO(image.image_data), media_type="image/jpeg")

'''This API is used to get a post by ID i.e, to search and get posts based on their IDs'''
@router1.get("/{T_ID}", status_code=status.HTTP_201_CREATED, response_model=TextsToneResponse)
def get_post(T_ID: int, db: Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    message = db.query(TextsTone).filter(TextsTone.T_ID == T_ID, TextsTone.Owner_id == current_user.U_ID).first()
    
    print(message)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {T_ID} not found")
    return message


'''This API is used to delete a post by ID'''
@router1.delete("/{T_ID}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(T_ID: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"Current user ID: {current_user.U_ID}")  # Debug print
    print(f"Post ID to delete: {T_ID}")  # Debug print
    
    message_query = db.query(TextsTone).filter(TextsTone.T_ID == T_ID)
    message = message_query.first()
    
    print(f"Message found: {message}")  # Debug print
    
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {T_ID} not found")
    
    if message.Owner_id != current_user.U_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    message_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
     
'''This API is used to update posts by a particular user'''
@router1.put("/{T_ID}", status_code=status.HTTP_200_OK, response_model=TextsToneResponse)
def update_posts(T_ID: int, texts_tone: TextsToneCreate, db: Session =  Depends(get_db), id : int = Depends(get_current_user)):
    message = db.query(TextsTone).filter(TextsTone.T_ID == T_ID).first()
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {T_ID} not found")
    for key, value in texts_tone.dict().items():
        setattr(message, key, value)
    db.commit()
    db.refresh(message)
    return message


                                                                                                                               