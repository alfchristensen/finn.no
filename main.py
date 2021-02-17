import finn_details
from gdocs import gdocs

# Variables
SHEET_ID = ''
TITLE = 'Toyota Land Cruiser'
FINN_SEARCH = 'https://www.finn.no/car/used/search.html?mileage_to=300000&model=1.813.1397&price_to=280000&registration_class=1&sort=PRICE_ASC&stored-id=46543826&year_from=2003'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # If modifying these scopes, delete the file token.pickle.

# initialize objects
gdocs = gdocs(SCOPES)
service = gdocs.authenticate()

# Get details from finn.no on each car matching the search
car_details = finn_details.get_car_details(FINN_SEARCH)
for car in car_details:
    print(car[:-1])

# Gain authentication to gdocs api
creds = gdocs.authenticate()

# Create if an ID is presented as a global variable
if not SHEET_ID:
    SHEET_ID = gdocs.create_sheet(service, TITLE)
    print(SHEET_ID)

# Update spreadsheet
response = gdocs.update_sheet(creds, SHEET_ID)
print(response)