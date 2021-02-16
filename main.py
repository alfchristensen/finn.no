import finn_details

# Variables
finn_search = 'https://www.finn.no/car/used/search.html?mileage_to=300000&model=1.813.1397&price_to=280000&registration_class=1&sort=PRICE_ASC&stored-id=46543826&year_from=2003'

# Get details from finn.no on each car matching the search
car_details = finn_details.get_car_details(finn_search)

for car in car_details:
    print(car[:-1])
