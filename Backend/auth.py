from google_auth_oauthlib.flow import Flow

scopes = [
 "https://www.googleapis.com/auth/classroom.courses.readonly",
 "https://www.googleapis.com/auth/classroom.coursework.students.readonly"
]

flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=scopes,
    redirect_uri="http://localhost:8000/auth/callback"
)

