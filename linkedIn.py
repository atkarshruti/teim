import requests
import openpyxl
import codecs
import chardet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define your LinkedIn API credentials
client_id = "77lfhbwxaubcr2"
client_secret = "LSTQ4AA31qr7mAh9"
access_token = "AQWpolXstmzPPn-xna4lNb2tfnIe-XH7k1A0RHATduf4C9FDdDoleQUWNP9qQhdL8W2wCovbHPVKw2g3_ZbEkb4kSCC6kvlqFSXIIRHC09_FRvvdKOXhw0spWP6MW5iIqiU9soio7NiiSmZnWrwuj64cpTh91Tar7MW3p0hxLyHRetXJBxrp1l-fkHelJiheB4LWZUnz4coh7sxohiMer9E4Gm1iyVxB8HHH79JDN0q-afREoacJxfNKmGpIUEi3KEPSq67G3gnRQIIzq66sTVZtYa19g1aTYpsKxuazwYOYEHXia7qbPaJjzo7tHGg_ITpdaewv04nIct2JvCSpKybcgx_xGw"
# Obtained through OAuth2

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('group1-marketanalysis.json', scope)
client = gspread.authorize(credentials)


# Make a request to get the user's profile data
# profile_url = "https://api.linkedin.com/v2/me"
profile_url = "https://api.linkedin.com/v2/userinfo"
headers = {
    "Authorization": f"Bearer {access_token}",
}
response = requests.get(profile_url, headers=headers)

if response.status_code == 200:
    profile_data = response.json()


    # Open the Google Sheet by title
    sheet = client.open('Linkedindata')

    # Select the specific worksheet within the Google Sheet
    worksheet = sheet.get_worksheet(0)  # 0 represents the first worksheet

    linkedin_data_to_save = [
        [ "Name","Surname", "Email"],
        [profile_data.get( "given_name"), profile_data.get("family_name"), profile_data.get("email")]
    ]

    worksheet.update('A1', linkedin_data_to_save)
    print(
        f"Data from the LinkedIn has been successfully fetched and stored in the Google Sheet '{sheet}'.")


else:
    print("Error fetching LinkedIn profile data:", response.status_code)
    print("Response content:", response.text)
    print("Response Content:", response.content.decode('utf-8'))