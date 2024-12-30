import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Scopes nécessaires
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def gmail_authenticate():
    creds = None

    # Vérifie si un token existe et charge les credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Rafraîchit les credentials ou lance un nouveau flux OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0, access_type="offline")
        # Enregistre les nouveaux credentials
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    print("Authentification réussie, vous pouvez maintenant utiliser l'API Gmail.")
    return service

if __name__ == "__main__":
    service = gmail_authenticate()
