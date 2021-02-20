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
        return spreadsheet['spreadsheetId']

    def read_sheet(self, service, SHEET_ID, cell_range):
        result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=cell_range).execute() 
        values = result.get('values', [])
        return values

    def append_sheet(self, service, SHEET_ID, values):
        
        response = service.spreadsheets().values().append(spreadsheetId=SHEET_ID, range='Sheet1!A1:M1', valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body={'values': [values]}).execute()
        print(response)


    def update_sheet(self, service, SHEET_ID):

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SHEET_ID, range='Sheet1!A1:A100').execute() 
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Registration:')
            for row in values:
                print(row)
                # Print columns A and E, which correspond to indices 0 and 4.
                #print('%s, %s' % (row[0], row[4]))

        return ''