import finn
from gdocs import gdocs

# Variables
SHEET_ID = '1eS8pd8LKE1dOaCwm9FQhjF9d3perWmCV1LK95nRcSvQ'
TITLE = 'Toyota Land Cruiser'
FINN_SEARCH = 'https://www.finn.no/car/used/search.html?mileage_to=300000&model=1.813.1397&price_to=280000&registration_class=1&sort=PRICE_ASC&stored-id=46543826&year_from=2003'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # If modifying these scopes, delete the file token.pickle.
CELL_RANGE = 'Sheet1!A1:T100'
existing_registration = []
existing_chassis = []

# initialize objects
gdocs = gdocs(SCOPES)
service = gdocs.authenticate()
"""
# Get details from finn.no on each car matching the search
car_details = finn.get_car_details(FINN_SEARCH)
    
# Retrieve existing data if sheet ID is supplied. If not, create a new spreadsheet 
if SHEET_ID:
    # Obtain key data from existing spreadsheet
    existing_data = gdocs.read_sheet(service, SHEET_ID, CELL_RANGE)

    for row in existing_data:
        print(row)
        try:
            existing_registration.append(row[0])
        except IndexError:
            pass
        try:
            existing_chassis.append(row[1])
        except IndexError:
            pass
else:
    # Create new spreadsheet
    SHEET_ID = gdocs.create_sheet(service, TITLE)

# Update spreadsheet
for car in car_details:
    if car[0] in existing_registration:
        # update row
        pass
    elif car[1] in existing_chassis:
        # update row
        pass
    else:
        # append row
        pass
"""

gdocs.append_sheet(service, SHEET_ID)










#print(existing_registration)
#print(existing_chassis)

#for row in existing_data:
#    print([row[0]])

#print(response)

# Gain authentication to gdocs api
#creds = gdocs.authenticate()

# Update spreadsheet
#response = gdocs.update_sheet(service, SHEET_ID)