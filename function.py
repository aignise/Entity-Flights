import requests
from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ENDPOINT = 'https://priceline-com-provider.p.rapidapi.com/v1/flights/search'

def search_cheapest_flight(origin_location, destination_location, departure_date, passenger_count):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    }

    querystring = {
        "location_arrival": destination_location,
        "date_departure": departure_date,
        "sort_order": "PRICE",
        "class_type": "ECO",
        "location_departure": origin_location,
        "itinerary_type": "ONE_WAY",
        "price_max": "20000",
        "duration_max": "2051",
        "price_min": "100",
        "date_departure_return": "2024-07-25",
        "number_of_stops": "0",
        "number_of_passengers": passenger_count
    }

    try:
        response = requests.get(ENDPOINT, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        if 'flights' in data:
            flights = data['flights']
            if not flights:
                return "No flights found."

            cheapest_flight = min(flights, key=lambda x: x['price'])
            return cheapest_flight
        else:
            return "No flight offers found in response."
    except requests.RequestException as e:
        return "Error fetching data: {}".format(e)

def get_location_id(location_name):
    url = "https://priceline-com-provider.p.rapidapi.com/v1/flights/locations"
    querystring = {"name": location_name}
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if isinstance(data, list) and data:  
        location_info = data[0]  
        location_id = location_info.get('id')  
        return location_id
    else:
        return None
