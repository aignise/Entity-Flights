# Flight Assistant Bot

Flight Assistant Bot is a bot that helps users find the cheapest flights based on their criteria.
This Python program utilizes OpenAI's GPT-4 model to create a flight search assistant. It helps users find the cheapest flight based on their criteria.

## Functionality
The assistant provides the following functionality:
- Search for the cheapest flight based on user input.
- Retrieve flight information such as price, departure time, arrival time, airline, and flight number.

## Arguments
The assistant function, `search_cheapest_flight`, requires the following arguments:
- `origin_location`: Departure airport location.
- `destination_location`: Arrival airport location.
- `departure_date`: Date of departure in the format YYYY-MM-DD.
- `passenger_count`: Number of passengers.

## Steps to Run the Program
1. Ensure you have Python installed on your system.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Obtain an OpenAI API key and set it as an environment variable named `OPENAI_API_KEY` in a `.env` file.
4. Obtain an OpenAI assistant ID and set it as an environment variable named `ASSISTANT_ID` in the `.env` file.
5. Run the program by executing the `main.py` file.
6. Enter your origin location, destination location, departure date, and the number of passengers when prompted.
7. The program will provide information about the cheapest flight based on your criteria.


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





