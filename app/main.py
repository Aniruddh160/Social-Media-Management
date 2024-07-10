'''Importing all the necessary Packages:'''


#To display resoponse (HTTP SERVER REQS)
from fastapi import FastAPI, Response, status, HTTPException, Depends

#To create a body for the Post method path
from fastapi.params import Body

#base model defines what the receiver is displayed
from pydantic import BaseModel

#For ratings and published
from typing import Optional

#For Id of post
from random import randrange

#Importing psycopg2 (python and postgresql adapter)
import psycopg2
from psycopg2.extras import RealDictCursor 

#importing time module for making a program wait
import time


#Importing packages for creating a database and also to creat the model required
'''from sqlalchemy.orm import Session



#Structure of data
from .database import Base
from sqlalchemy.sql.expression import null
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, default=True)



#database 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aniruddhan11121@LocalPostgres/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()'''



#Creating an opbject for FastAPI
app = FastAPI() 




'''
This is a class that defines the BasicModel(Basic way of) representing a post.
'''
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None   



'''
This is done using psycopg2(adapter) that allows the database to integrate with the python program. 
'''
while True:
    try:
        conn = psycopg2.connect(host = 'localhost' , database='postgres', user = 'postgres',
                            password = 'Aniruddhan11121' ,cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection failed")
        print("error: ", error)
        time.sleep(2)




'''
This is a list of dictionaries which are some hardcoded posts. These are already added and are accessed
by a get_posts method.
'''
my_posts = [{"title" : "hello everybody", "contents" : "Feels good to be here", "id" : 1},
            {"title" : "meet my dog", "contents" : "He says hi!!", "id" : 2}]




'''
This APi is used as the root directory. The first message we can view when we open the path 
http://127.0.0.1:8000/.
'''
@app.get("/")
async def root():
    
    return {"message": "Welcome to FastAPI!!"}

'''
This API call is to test the 'Session'
'''

'''@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status" : "Success"}'''

    




'''
This API is the get_posts method which allows us to access posts that are already hardcoded and also posts
which are added by using the create_posts method.
'''
'''@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}'''

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}


'''
This function allows the user to find the post of a specific ID. It is a simple for loop which returns the 
post of the specific ID.
'''
def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            print(p)
            return p
            


'''
This function is the reverse of the previous one where we can find the ID of a sepcific post.
'''
def find_post_ID(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
                    
                    
'''
This is the create_posts API which allows the user to post 'posts'/ create posts. 
'''

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    cursor.execute(f"""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s)RETURNING *""", (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    
    conn.commit()
    return {"data": new_post}



'''
This API is used to get a post by using its specified ID. We give the http req to find a post with the
ID along - /posts/{id}. This will get us the required post. Here we use the find_post() function 
'''
@app.get("/posts/{id}")
def get_post(id: int, response : Response):
    
    cursor.execute(""" SELECT * FROM posts WHERE ID = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        response.status_code = 404
        print(post)
        return {"post_details" : f"post with id : {id} was not found!!"}
    return post




'''
This API is used to delete posts which are added. For example when we add post we can see all the posts 
we have added using the get_posts API call view the posts and later delete unwanted posts. 
'''
@app.delete("/posts/{id}", status_code=status.HTTP_201_CREATED)
def delete_posts(id: int):
    
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
   
    '''
    This is to raise an HTTPException to tell the user that the post they are searching for is unavailable.
    '''
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
    


'''
This API call is to update a post which has already been added. Here we use a variable post_dict that stores
the post that the user is searching for and then sets id of the post and later rewrites the post into post_dict.
'''    
@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
    
    return{ "data" : updated_post}
    
