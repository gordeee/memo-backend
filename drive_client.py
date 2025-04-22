from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/documents.readonly']

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def get_docs_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build('docs', 'v1', credentials=creds)

def get_memo_files():
    service = get_drive_service()

    # Replace this with your actual shared drive ID
    SHARED_DRIVE_ID = "0AG4puY_yV2C7Uk9PVA"

    query = "name contains 'Memo'"

    results = service.files().list(
        q=query,
        driveId=SHARED_DRIVE_ID,
        corpora="drive",
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        fields="files(id, name, mimeType, modifiedTime)",
        pageSize=100
    ).execute()

    return results.get('files', [])
# Placeholder for Google Drive client integration
