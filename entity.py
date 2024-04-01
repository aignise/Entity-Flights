import os
import time
from dotenv import load_dotenv
import openai
from function import search_cheapest_flight, get_location_id

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

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

def create_thread():
    thread = client.beta.threads.create()
    return thread.id

def start(thread_id, user_query):
    content = f"Origin Location: {user_query['origin_location']}, Destination Location: {user_query['destination_location']}, Departure Date: {user_query['departure_date']}, Passenger Count: {user_query['passenger_count']}"
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def get_response(thread_id, assistant_id, user_query):
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

def submit_tool_outputs(thread_id, run_id, run_status, user_query):
    output = search_cheapest_flight(**user_query)  
    
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
    
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )

def main():
    thread_id = create_thread()
    origin_location = input("Enter your origin location: "),
    destination_location = input("Enter your destination location: "),
    
    origin = get_location_id(origin_location)
    destination = get_location_id(destination_location)
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
