from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from db import get_db
import db_models
import json
from sqlalchemy.orm import Session

with open("credentials.json") as f:
    creds_data = json.load(f)

client_id = creds_data["web"]["client_id"]
client_secret = creds_data["web"]["client_secret"]

user_router = APIRouter()

def fetch_all_files(drive_service, folder_id, all_files=None, depth=0):
    if all_files is None:
        all_files = []
    
    if depth > 5:  # stop at 5 levels deep
        return all_files

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get("files", [])

    for item in items:
        all_files.append(item)
        if item["mimeType"] == "application/vnd.google-apps.folder":
            fetch_all_files(drive_service, item["id"], all_files, depth+1)

    return all_files

@user_router.get("/users/u{id}/pyqs")
def pyqs(id, db: Session = Depends(get_db)):

    user = db.query(db_models.User).filter(db_models.User.id == id).first()

    if not user:
        return RedirectResponse("/login")

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    drive_service = build("drive", "v3", credentials=credentials)
    files = fetch_all_files(drive_service, "1cyTmrlABGwaP81sStbZM16enFITtswTI")
    if not user:
        return {"error": "user not found", "id": id}
    return {"files": files}


from ml import extract_text_from_pdf, match_notes_to_pyqs
import re

@user_router.get("/users/u{id}/sync-pyqs")
def sync_pyqs(id, folder_id: str, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        return RedirectResponse("/login")

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    drive_service = build("drive", "v3", credentials=credentials)
    files = fetch_all_files(drive_service, folder_id)

    saved = 0
    for f in files:
        if f["mimeType"] != "application/pdf":
            continue
        exists = db.query(db_models.PYQFile).filter(db_models.PYQFile.file_id == f["id"]).first()
        if exists:
            continue
        year_match = re.search(r'20\d{2}', f["name"])
        year = int(year_match.group()) if year_match else None
        text = extract_text_from_pdf(drive_service, f["id"])
        db.add(db_models.PYQFile(
            file_id=f["id"],
            name=f["name"],
            mime_type=f["mimeType"],
            user_id=int(id),
            extracted_text=text,
            year=year
        ))
        saved += 1

    db.commit()
    return {"synced": saved}


@user_router.post("/users/u{id}/match-notes")
def match_notes(id, notes: str, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        return RedirectResponse("/login")

    pyq_files = db.query(db_models.PYQFile).filter(
        db_models.PYQFile.user_id == int(id),
        db_models.PYQFile.extracted_text != None
    ).all()

    pyq_texts_with_years = [
        {"text": f.extracted_text, "year": f.year or 0}
        for f in pyq_files
    ]

    results = match_notes_to_pyqs(notes, pyq_texts_with_years)
    return {"tagged_chunks": results}