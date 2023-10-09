import requests
import openpyxl
import codecs
import chardet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('group1-marketanalysis.json', scope)
client = gspread.authorize(credentials)

# Define your credentials
client_id = ""
client_secret = ""
access_token = "EAAXduZCvr1F4BO5XnpeAbStQJlJBKvpTJ9G8KuK8WQFo4mpeJZCH1txI8TSPSljZCA6ZBnkmbmf0Dl14KC98TcOolDTdbrBG3vhJm42UDaawGPX1XqEPZCcRXAPUwkuBW41PSuNzebB3pBQPcoM6emahj05cDvF2qskddzsYYVmHZBVl2vuX9rcZCb1TA9f8xsfruZCEUuUrx1IkeO0ccdWnU5wMCE2PKuFA7sZCXiex6ThZABuD2jGtseMYaWxGOXHBrgkAZDZD"
# Make a request to get the user's profile data
profile_url = "https://graph.facebook.com/v18.0/me?fields=id%2Cname%2Cgender%2Cemail%2Cbirthday&access_token=" + access_token
response = requests.get(profile_url)

if response.status_code == 200:
    profile_data = response.json()

    # Access the worksheet in the spreadsheet
    worksheet = client.open('Facebookdata')

    # Select the specific worksheet within the Google Sheet
    worksheet = worksheet.get_worksheet(0)  # 0 represents the first worksheet

    facebook_data_to_save = [
        [ "id","name", "gender","email","birthday"],
        [profile_data.get( "id"), profile_data.get("name"), profile_data.get("gender"),profile_data.get("email"),profile_data.get("birthday")]
    ]

    worksheet.update('A1', facebook_data_to_save)
    print(
        f"Data has been successfully fetched and stored in the Google Sheet '{SHEET_NAME}'.")


else:
    print("Error fetching LinkedIn profile data:", response.status_code)
    print("Response content:", response.text)
    print("Response Content:", response.content.decode('utf-8'))