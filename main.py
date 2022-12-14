from __future__ import print_function
from dotenv import load_dotenv
from datetime import date
# from plyer import notification
import os
from traceback import print_exc

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from get_emails import get_emails

load_dotenv()

# EDIT IF NEEDED
DATE = date(2023, 1, 2)  # year, month, day
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv('SHEET_NAME')


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
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        except:
            get_emails()
            raise FileNotFoundError('credentials.json not found, emails saved in out/emails.csv')

        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('sheets', 'v4', credentials=creds)
    range_name = f'{SHEET_NAME}!H:H'

    # Reading
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=range_name).execute()
    values = result.get('values', [])

    if not values:
        raise Exception('Check if you have the correct sheet selected.')

    emails, count = get_emails()

    emails_range = f'{SHEET_NAME}!D{len(values) + 1}:H{len(values) + count + 1}'
    date_range = f'{SHEET_NAME}!C{len(values) + 1}:C{len(values) + count + 1}'
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
    print_exc(e)
    print('Error; emails stored in out/emails.csv')


# notification.notify(
#     title = 'Plexmailer',
#     message = 'Done!',
#     app_icon = None,
#     timeout = 10
# )