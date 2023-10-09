import os
import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set your YouTube Data API Key
YOUTUBE_API_KEY = 'AIzaSyDTLuCPu1dau9izhnAIItQxSzhL3KfRm60'

# Set the YouTube Channel ID you want to fetch data from
CHANNEL_ID = 'UCI0r1JJ4YkvDsh-2bXc5tBw'

# Set the name of the Google Sheet where you want to store the data
SHEET_NAME = 'Youtubedata'

# Authenticate with YouTube Data API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('group1-marketanalysis.json', scope)
gc = gspread.authorize(credentials)

# Get the YouTube channel's uploads playlist ID
try:
    channel_response = youtube.channels().list(part='contentDetails', id=CHANNEL_ID).execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the video details from the uploads playlist
    playlist_items_response = youtube.playlistItems().list(
        part='snippet',
        maxResults=50,  # You can adjust the number of videos to fetch per request
        playlistId=uploads_playlist_id
    ).execute()

    # Create or open the Google Sheet
    try:
        worksheet = gc.open(SHEET_NAME)
    except gspread.exceptions.SpreadsheetNotFound:
        worksheet = gc.create(SHEET_NAME)

    # Select the first sheet in the Google Sheet
    worksheet = worksheet.get_worksheet(0)

    # Clear existing data in the sheet
    worksheet.clear()

    # Write the headers to the Google Sheet
    headers = ['Video Title', 'Video Description', 'Video ID', 'Published At']
    worksheet.append_row(headers)

    # Fetch and store video data in the Google Sheet
    for item in playlist_items_response['items']:
        video_title = item['snippet']['title']
        video_description = item['snippet']['description']
        video_id = item['snippet']['resourceId']['videoId']
        published_at = item['snippet']['publishedAt']

        row_data = [video_title, video_description, video_id, published_at]
        worksheet.append_row(row_data)

    print(f"Data from the YouTube channel {CHANNEL_ID} has been successfully fetched and stored in the Google Sheet '{SHEET_NAME}'.")

except HttpError as e:
    print(f"An error occurred: {e}")
