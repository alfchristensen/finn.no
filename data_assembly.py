import finn
import listprice
import data_assembly

def generate_datasets(finn_search):

    car_list = finn.get_car_details(finn_search)

    # Add list price
    for car in car_list:
        print(car)
        if car[0] and car[3]:
            regnr = car[0]
            km = str(car[3])
            print(regnr, km)
            listprice = listprice.get_listprice(regnr, km)
            print(listprice)
            #car[12] = listprice

    #return car_list