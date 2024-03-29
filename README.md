# Flight Assistant Bot

Flight Assistant Bot is a bot that helps users find the cheapest flights based on their criteria.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/flight-assistant-bot.git
   cd flight-assistant-bot
Install dependencies:

bash
- pip install -r requirements.txt

## Set up environment variables:

Create a .env file in the root directory and add the following:

OPENAI_API_KEY=your_openai_api_key
RAPIDAPI_KEY=your_rapidapi_key
ASSISTANT_ID=your_assistant_id


## Run the Flask app:

bash
Copy code
python app.py

### Usage
Send a POST request to /flight/search endpoint with JSON data containing origin location, destination location, departure date, and passenger count. The response will contain flight information.

## Example:

json

{
  "origin_location": "New York",
  "destination_location": "Los Angeles",
  "departure_date": "2024-04-01",
  "passenger_count": 2
}

## License
This project is licensed under the MIT License - see the LICENSE file for details.





