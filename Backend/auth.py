from urllib import response
import requests     # For getting user email using request
from google_auth_oauthlib.flow import Flow
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
from db import get_db
from sqlalchemy.orm import Session
import db_models

scopes = [
 "https://www.googleapis.com/auth/classroom.courses.readonly",
 "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
 "https://www.googleapis.com/auth/userinfo.email",
 "openid" 
]

flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=scopes,
    redirect_uri="http://localhost:8000/auth/callback"
)

auth_router= APIRouter()

@auth_router.get("/login")
def login():

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )
    return RedirectResponse(authorization_url)

@auth_router.get("/auth/callback")
def auth_callback(request: Request, db:Session = Depends(get_db)):
    # Creates a New login session
    flow.fetch_token(authorization_response = str(request.url))
    credentials = flow.credentials
    access_token = credentials.token
    refresh_token = credentials.refresh_token
    expiry = credentials.expiry     
    response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"}
    )
    user_info = response.json()
    user_email = user_info["email"]
    
    exists = db.query(db_models.User).filter( db_models.User.user_email == user_email).first()

    if exists:
        exists.access_token = access_token
        exists.refresh_token = refresh_token
        exists.expiry = expiry

    else:
        db.add(db_models.User(
            user_email = user_email,
            access_token = access_token,
            refresh_token = refresh_token,
            expiry = expiry
        ))
    db.commit()

    return {"message": "OAuth Successful"}

