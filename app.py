from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure generative AI with your API key
genai.configure(api_key="AIzaSyApdIIDxko0YfMZ_xMatRdFSfXN2eaY8WI")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    data = request.json  
    user_input = data['user_input']  # Input from html file
    bot_response = chatbot_interaction(user_input)
    return jsonify({'bot_response': bot_response})

def book_test_drive(make, model, year, date, time):
    return f"Test drive booked for {make} {model} {year} on {date} at {time}."

def find_nearby_dealerships(location):
    return f"Nearest car dealerships to {location} are: Dealership A, Dealership B, Dealership C."

def provide_car_buying_advice(budget):
    return "Car buying advice: Consider fuel efficiency, safety features, and resale value when choosing a car within your budget."

def chatbot_interaction(user_input):
    convo = model.start_chat(history=[])
    convo.send_message(user_input)
    return convo.last.text

if __name__ == '__main__':
    app.run(debug=True)
