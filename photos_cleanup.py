import os
import sys
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# Required scopes for read + delete app-created media
SCOPES = [
    "https://www.googleapis.com/auth/photoslibrary.readonly",
    "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata"
]

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def authenticate(force_refresh=False):
    creds = None

    if force_refresh and os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("Old token deleted. Forcing fresh authentication...")

    # Load token if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Authenticate if token is missing or invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_credentials_file(
                CREDENTIALS_FILE,
                scopes=SCOPES
            )
            # Force a static redirect URI by fixing the port
            creds = flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message="")

        # Save new token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def list_photos(service, page_size=10):
    try:
        results = service.mediaItems().list(
            pageSize=page_size
        ).execute()
        items = results.get('mediaItems', [])

        if not items:
            print("No media items found.")
        else:
            for item in items:
                print(f"{item['filename']} - {item['id']}")

    except HttpError as error:
        print(f"API error: {error}")

def main():
    force
 