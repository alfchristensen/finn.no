from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class gdocs:

    def __init__(self, scopes): 
        self.scopes = scopes
    
    def authenticate(self):
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Creating and returning connection
        service = build('sheets', 'v4', credentials=creds)
        return service

    def create_sheet(self, service, title):
        spreadsheet = {
            'properties': {
                'title': f'{title}'
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        #print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        return spreadsheet['spreadsheetId']

    def update_sheet(self, service, SHEET_ID):
        return ''