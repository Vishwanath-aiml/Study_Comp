from fastapi import APIRouter, Depends, Session
from fastapi.responses import RedirectResponse
from google.oauth2.credentials import Credentials  # To use class Credentials that does the refresh_token thingy for us
from googleapiclient.discovery import build # to build that is access data from drive
from db import get_db
import db_models
import json

# Get the client id and secret
with open("credentials.json") as f:
    creds_data = json.load(f)

client_id = creds_data["web"]["client_id"]
client_secret = creds_data["web"]["client_secret"]

user_router = APIRouter()

@user_router.get("/users/u{id}/pyqs")
def pyqs(id, db: Session = Depends(get_db())):
    
    user = db.query(db_models.User).filter(db_models.User.id == id) # Fetches User details

    if not user:
        return RedirectResponse("/login")  # if User not logged in redirect to login page

    credentials = Credentials(
    token = user.access_token,
    refresh_token = user.refresh_token,
    token_uri = "https://oauth2.googleapis.com/token",
    client_id = client_id,
    client_secret = client_secret
    )

