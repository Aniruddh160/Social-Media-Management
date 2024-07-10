from passlib.context import CryptContext
import requests
from fastapi import HTTPException, status
import os
import google.generativeai as genai



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_verified = pwd_context.verify(plain_password, hashed_password)
    print(f"Verifying password: {plain_password} with hash: {hashed_password} - Result: {is_verified}")
    return is_verified



def verify_content(title: str, content: str) -> bool:
    # Fetch the API key from environment variables
    API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDNs_3Ov1iAVEL19-1hrEMXqqua7Zcntcs")
    
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key for Gemini is not configured."
        )

    # Configure the generative AI client with the API key
    genai.configure(api_key=API_KEY)
    
    # Create the GenerativeModel object
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    
    try:
        # Generate a response for the content
        print(f"Sending to Gemini API: Title: {title}, Content: {content}")  # Debug print
        prompt = f"""Question: Consider this particular title "He's very bad" and this content "He's a dick". Based on this title and content, Identify whether the message is harmful or not.
Answer: Harmful

Question: Consider this particular title "He's can improve" and this content "He's growing a lot". Based on this title and content, Identify whether the message is harmful or not.
Answer: Not Harmful

Question: Consider this particular title "{title}" and this content "{content}". Based on this title and content, Identify whether the message is harmful or not.
Answer: """
        response = model.generate_content(prompt)
        
        # Debug print the raw response from the API
        print(f"Response from Gemini API: {response.text}")
        print(response.text.lower())
        
        # Determine if the content is harmful based on the API's response
        if "not harmful" in response.text.lower():
            return True
        else:
            return False
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying content: {str(e)}"
        )
        
        
        
