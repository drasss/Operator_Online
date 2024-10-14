# cd E:"\programme\projet d'envergure\streamlit orga\1.0\"Operator_Online

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

credential_path = """Credentials.json"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1szbNj6_bH4mA9HsBIJD-qKyrNFYwYyEqG-ekmoGnE5A'

creds=gsheet_api_check(SCOPES)

from googleapiclient.discovery import build
def pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=ranging).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=ranging).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data
    
#----------------------------------------------------------------------------
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def update_values(spreadsheet_id, range_name, value_input_option, _valued):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)
    values = [[""]*6]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
    # Pass: spreadsheet_id, range_name value_input_option and _values)
    service = build("sheets", "v4", credentials=creds)

    values = [["Test","A","B","C","D","E"]]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId="1szbNj6_bH4mA9HsBIJD-qKyrNFYwYyEqG-ekmoGnE5A",
            range="A3:F3",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute())

#----------------------------------------------------------------------------
import pandas as pd



ranging = 'A1:F100'
data = pull_sheet_data(SCOPES,SPREADSHEET_ID,ranging)
df = pd.DataFrame(data)


