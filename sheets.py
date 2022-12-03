from __future__ import print_function
from dotenv import load_dotenv
from datetime import date
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from get_emails import get_emails

load_dotenv()

# EDIT IF NEEDED
DATE = date(2022, 11, 28)
SPREADSHEET_ID = '1b1ntUFHoT3rJFqelbjrRODS8_FQ0o7jwEqZCjgJxikE'

def sheets():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        range_name = 'Shamith!H:H'

        # Reading
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=range_name).execute()
        values = result.get('values', [])

        if not values:
            raise Exception('Check if you have the correct sheet selected.')

        emails, count = get_emails()

        emails_range = f'Shamith!D{len(values) + 1}:H{len(values) + count + 1}'
        date_range = f'Shamith!C{len(values) + 1}:C{len(values) + count + 1}'
        data = [
            {
                'range': emails_range,
                'values': emails
            },
            {
                'range': date_range,
                'values': [[f'{DATE.month}/{DATE.day}/{DATE.year}']] * count
            }
        ]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

    except Exception as e:
        print(e)
        print('Error; emails stored in out/emails.csv')
