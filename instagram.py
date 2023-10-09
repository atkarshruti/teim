import requests
import pandas as pd
import openpyxl
import codecs
import chardet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('group1-marketanalysis.json', scope)
client = gspread.authorize(credentials)
# Define your credentials
# client_id = "6537860372969905"
client_secret = ""
access_token = "IGQWRPaGFDcHpNblBiaF9IaG1YOFdpbm1PSG5laEg1eFhxMk9WN3I5bTVjZAjlxR2ZAkcDFyUE1sUTVVOHppRHQ1cXpyaWFERGNoS3M0VWM0dktZAd3ZAVa3BEaFFYRlpGNDhnOGtFRHAwTG9HN3RvVHFvQlBlTWpESWdnVC1YdFJ2Q2VtQQZDZD"

# Make a request to get the user's profile data
profile_url = "https://graph.instagram.com/v18.0/6537860372969905/media?fields=id,media_type,media_url,username,timestamp&access_token=IGQWRPaGFDcHpNblBiaF9IaG1YOFdpbm1PSG5laEg1eFhxMk9WN3I5bTVjZAjlxR2ZAkcDFyUE1sUTVVOHppRHQ1cXpyaWFERGNoS3M0VWM0dktZAd3ZAVa3BEaFFYRlpGNDhnOGtFRHAwTG9HN3RvVHFvQlBlTWpESWdnVC1YdFJ2Q2VtQQZDZD"
response = requests.get(profile_url)

if response.status_code == 200:
    profile_data = response.json()

    # Access the worksheet in the spreadsheet
    worksheet = client.open('Instagramdata')

    # Select the specific worksheet within the Google Sheet
    worksheet = worksheet.get_worksheet(0)  # 0 represents the first worksheet

    insta_data_to_save = pd.DataFrame(profile_data["data"])

    gspread_dataframe = [insta_data_to_save.columns.values.tolist()] + insta_data_to_save.values.tolist()
    worksheet.update(gspread_dataframe, 2)
    print(
        f"Data has been successfully fetched and stored in the Google Sheet '{SHEET_NAME}'.")


else:
    print("Error fetching LinkedIn profile data:", response.status_code)
    print("Response content:", response.text)
    print("Response Content:", response.content.decode('utf-8'))