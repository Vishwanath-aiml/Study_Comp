from google_auth_oauthlib.flow import Flow
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from datetime import datetime

scopes = [
 "https://www.googleapis.com/auth/classroom.courses.readonly",
 "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly"
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
def auth_callback(request: Request):
    flow.fetch_token(authorization_response = str(request.url))
    credentials = flow.credentials
    access_token = credentials.token
    refresh_token = credentials.refresh_token
    expiry = credentials.expiry
    return {"message": "OAuth Successful"}

