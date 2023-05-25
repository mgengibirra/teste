import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

# Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account_file.json'

# Initialize Google Drive API client
creds = None
try:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
except HttpError as error:
    st.write(f"An error occurred: {error}")
    creds = None

# Streamlit app
def main():
    st.title("Google Drive File Manager")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a file to upload", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        try:
            # Create a new file in the user's Google Drive folder
            file_metadata = {'name': uploaded_file.name, 'parents': ['root']}
            media = googleapiclient.http.MediaIoBaseUpload(uploaded_file, mimetype=uploaded_file.type)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            st.success("File uploaded successfully!")
        except HttpError as error:
            st.write(f"An error occurred: {error}")
    
    # File download
    file_list = []
    try:
        # Get a list of files in the user's Google Drive folder
        results = drive_service.files().list(q="'root' in parents and trashed = false", fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            st.write('No files found in your Google Drive folder.')
        else:
            for item in items:
                file_list.append(item['name'])
    except HttpError as error:
        st.write(f"An error occurred: {error}")
    
    selected_file = st.selectbox("Choose a file to download", file_list)
    if selected_file:
        try:
            # Download the selected file from the user's Google Drive folder
            file_id = None
            results = drive_service.files().list(q="'root' in parents and trashed = false", fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            for item in items:
                if item['name'] == selected_file:
                    file_id = item['id']
                    break
            if file_id is not None:
                request = drive_service.files().get_media(fileId=file_id)
                file_contents = request.execute()
                st.download_button("Download file", file_contents, file_name=selected_file)
            else:
                st.write(f"File '{selected_file}' not found in your Google Drive folder.")
        except HttpError as error:
            st.write(f"An error occurred: {error}")

if __name__ == '__main__':
    main()
