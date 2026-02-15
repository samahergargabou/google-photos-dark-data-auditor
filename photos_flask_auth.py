import os
import pickle
from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)

# Update with your actual credentials filename
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'
SCOPES = [
    "https://www.googleapis.com/auth/photoslibrary.readonly",
    "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata"
]

# 1. Start auth flow
@app.route('/')
def authorize():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/callback'
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return redirect(auth_url)

# 2. Handle OAuth2 callback
@app.route('/callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/callback'
    )
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)

    return "✅ Authentication complete. You can close this tab."

# 3. Run the Flask server
if __name__ == '__main__':
    app.run('localhost', 8080, debug=True)
