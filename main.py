import time
import openai
import requests
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ENDPOINT = 'https://priceline-com-provider.p.rapidapi.com/v1/flights/search'

def setup():
    assistant = client.beta.assistants.create(
        name="Flight Search Assistant",
        instructions="You are a bot to help users find the cheapest flight based on their criteria.",
        model="gpt-4-turbo-preview", 
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "search_cheapest_flight",
                    "description": "Searches for the cheapest flight based on user input.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin_location": {
                                "type": "string",
                                "description": "Departure airport location"
                            },
                            "destination_location": {
                                "type": "string",
                                "description": "Arrival airport location"
                            },
                            "departure_date": {
                                "type": "string",
                                "description": "Date of departure (YYYY-MM-DD)"
                            },
                            "passenger_count": {
                                "type": "integer",
                                "description": "Number of passengers"
                            }
                        },
                        "required": ["origin_location", "destination_location", "departure_date", "passenger_count"]
                    }
                }
            }
        ]
    )

    return assistant.id

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
            print(cheapest_flight)
            return cheapest_flight
        else:
            return "No flight offers found in response."
    except requests.RequestException as e:
        return "Error fetching data: {}".format(e)

def create_thread():
    """Creates a thread for conversation."""
    thread = client.beta.threads.create()
    return thread.id

def start(thread_id, user_query):
    """Starts a conversation in the specified thread with the given user query."""
    content = f"Origin Location: {user_query['origin_location']}, Destination Location: {user_query['destination_location']}, Departure Date: {user_query['departure_date']}, Passenger Count: {user_query['passenger_count']}"
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def get_response(thread_id, assistant_id, user_query):
    """Retrieves the response from the OpenAI API."""
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Answer user questions using custom functions available to you."
    )
    
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == 'requires_action':
            submit_tool_outputs(thread_id, run.id, run_status, user_query)
        
        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value
    return response

def get_location_id(location_name):
    url = "https://priceline-com-provider.p.rapidapi.com/v1/flights/locations"
    querystring = {"name": location_name}
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if isinstance(data, list) and data:  # Check if data is a non-empty list
        location_info = data[0]  # Assuming there's only one location in the response
        location_id = location_info.get('id')  # Use get() to avoid KeyError
        print(location_id)
        return location_id
    else:
        return None


    
def submit_tool_outputs(thread_id, run_id, run_status, user_query):
    """Submits tool outputs to the OpenAI API."""
    output = search_cheapest_flight(**user_query)  # Fetch cheapest flight based on user input
    
    if isinstance(output, dict):
        output_str = f"Cheapest Flight Information:\nPrice: {output['price']} {output['currency']}\nDeparture Time: {output['departure_time']}\nArrival Time: {output['arrival_time']}\nAirline: {output['airline']}\nFlight Number: {output['flight_number']}"
    else:
        output_str = output
    
    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
    
    tool_outputs = []
    for tool_call in tool_calls:
        tool_outputs.append({
            "tool_call_id": tool_call.id,
            "output": output_str
        })
    
    # Submit tool outputs to OpenAI API
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )

def main():
    # Create a thread for conversation
    thread_id = create_thread()
    origin_location = input("Enter your origin location: "),
    destination_location = input("Enter your destination location: "),
    
    origin = get_location_id(origin_location)
    destination = get_location_id(destination_location)
    print(origin)
    print(destination)
    user_query = {
        "origin_location": origin,
        "destination_location": destination,
        "departure_date": input("Enter date of departure (YYYY-MM-DD): "),
        "passenger_count": int(input("Enter number of passengers: "))
    }
    
    assistant_id = os.getenv("ASSISTANT_ID")
    start(thread_id, user_query)

    response = get_response(thread_id, assistant_id, user_query)

    print("Flight Information:", response)


if __name__ == "__main__":
    main()
