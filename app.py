from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

app = Flask(__name__)

@app.route('/flight/search', methods=['POST'])
def search_flight():
    data = request.json
    origin_location = data.get('origin_location')
    destination_location = data.get('destination_location')
    departure_date = data.get('departure_date')
    passenger_count = data.get('passenger_count')

    assistant_id = os.getenv("ASSISTANT_ID")

    response = get_response(assistant_id, origin_location, destination_location, departure_date, passenger_count)

    return jsonify({"response": response})

def get_response(assistant_id, origin_location, destination_location, departure_date, passenger_count):
    # Logic to interact with the flight assistant bot
    # You can use the existing functions or modify as needed
    return "Flight information will be here"

if __name__ == "__main__":
    app.run(debug=True)
