import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials as SJAC

json_key = json.load(open('client_secret.json')) # json credentials you downloaded earlier
scope = ['https://spreadsheets.google.com/feeds']

credentials = SJAC(json_key['client_id'], json_key['client_secret'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google
sheet = file.open("test").sheet1 # open sheet



'''
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute()

range_names = [
  # Range names ...
]
result = service.spreadsheets().values().batchGet(
    spreadsheetId=spreadsheet_id, ranges=range_names).execute()

values = [
    [
        # Cell values ...
    ],
    # Additional rows ...
]
body = {
  'values': values
}
result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption=value_input_option, body=body).execute()


'''
