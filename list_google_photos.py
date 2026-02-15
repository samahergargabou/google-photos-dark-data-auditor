from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pickle

def get_authenticated_service():
    with open("token.pkl", "rb") as token:
        creds = pickle.load(token)
    return build("photoslibrary", "v1", credentials=creds, static_discovery=False)

def list_filenames():
    service = get_authenticated_service()
    filenames = []

    next_page_token = ''
    while next_page_token is not None:
        results = service.mediaItems().list(
            pageSize=100,
            pageToken=next_page_token
        ).execute()

        items = results.get("mediaItems", [])
        for item in items:
            filename = item.get("filename")
            if filename:
                filenames.append(filename)

        next_page_token = results.get("nextPageToken")
        if not next_page_token:
            break

    return filenames

if __name__ == "__main__":
    filenames = list_filenames()
    with open("google_photos_filenames.txt", "w", encoding="utf-8") as f:
        for name in filenames:
            f.write(name + "\n")

    print(f"Fetched {len(filenames)} filenames from Google Photos.")
