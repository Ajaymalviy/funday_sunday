from django.shortcuts import render, redirect
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
import os
import requests
from django.http import HttpResponse



CLIENT_SECRET_FILE = 'photos/client_secret_97064536251-lhhsolefvph5ql15j96el005el9pti2o.apps.googleusercontent.com.json'  # Path to your client secret file
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly', 'https://www.googleapis.com/auth/photoslibrary.append']


def home(request):
    return HttpResponse("done")

from google_auth_oauthlib.flow import InstalledAppFlow
from django.shortcuts import redirect
from django.http import HttpResponse

def start_oauth(request):
    # Initialize the flow with your client secret file and the necessary scopes
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    print(f"Redirecting to: {flow.authorization_url()[0]}")  # Log the auth URL

    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')  # Ensure correct prompt

    # Redirect the user to the Google OAuth URL
    return redirect(auth_url)

def oauth2callback(request):
    print("Inside oauth2callback")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    print('OAuth flow initialized')

    # Log the full authorization response
    authorization_response = request.build_absolute_uri()
    print('Authorization response: ', authorization_response)

    # Log request GET parameters
    print('Request GET parameters: ', request.GET)

    # Check for 'code' parameter
    if 'code' not in request.GET:
        error_message = "Error: Missing 'code' parameter in the callback URL."
        print(error_message)
        return HttpResponse(error_message)  # Return an error message for debugging

    try:
        # Fetch the token using the authorization code from the URL
        creds = flow.fetch_token(authorization_response=authorization_response)
        print('Credentials fetched: ', creds)

        # Save credentials in session
        request.session['credentials'] = creds.to_json()

        # Redirect to the list_photos view
        return redirect('list_photos')

    except Exception as e:
        print(f"Error during OAuth callback: {str(e)}")
        return HttpResponse(f"An error occurred: {str(e)}")  # Return an error message for debugging

# List photos in the authenticated user's Google Photos account
def list_photos(request):
    creds = Credentials.from_authorized_user_info(request.session['credentials'])
    service = build('photoslibrary', 'v1', credentials=creds)

    # Fetch photos from the user's Google Photos library with pagination support
    photos = []
    next_page_token = None
    while True:
        results = service.mediaItems().list(pageSize=100, pageToken=next_page_token).execute()
        photos.extend(results.get('mediaItems', []))
        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break

    return render(request, 'photos/list_photos.html', {'photos': photos})

# Upload selected photos to another Google Photos account
def upload_photos(request):
    creds = Credentials.from_authorized_user_info(request.session['credentials'])
    service = build('photoslibrary', 'v1', credentials=creds)
    
    # Example of selecting the photos to upload (you can modify this part based on your use case)
    selected_photos = request.POST.getlist('selected_photos')  # Assuming you send a list of photo IDs in a form

    for photo_id in selected_photos:
        # Fetch the photo details from the source account
        photo = service.mediaItems().get(mediaItemId=photo_id).execute()

        # Download the photo's original file
        file_data = requests.get(photo['baseUrl'] + '=d').content

        # Upload the photo to another Google Photos account (target account)
        media = service.mediaItems().upload(
            media_body=file_data,
            media_mime_type='image/jpeg'
        ).execute()

    return redirect('list_photos')
