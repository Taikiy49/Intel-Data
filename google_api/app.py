from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from datasets import load_dataset

app = Flask(__name__)

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyApdIIDxko0YfMZ_xMatRdFSfXN2eaY8WI")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

car_reviews_dataset = load_dataset("florentgbelidji/car-reviews")

# Helper function to query the database
def get_car_review(year, word):
    car_review = car_reviews_dataset["train"].filter(lambda example: 'Toyota' in example["Vehicle_Title"] and year in example["Vehicle_Title"].split()[:] and (word in example["Review"].split()[:] or word.capitalize() in example["Review"].split()[:]))
    num_car_reviews = len(car_review)
    if len(car_review) > 0:
        return [car_review[0]["Review"], num_car_reviews]
    else:
        return [None, 0]

# Function to handle regular chatbot interactions
def chatbot_interaction(user_input):
    convo = model.start_chat(history=[])
    convo.send_message(user_input)
    return convo.last.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('input', '')
    if "!find" in user_input.lower():
        return jsonify({'message': "Please provide the year and model."})
    else:
        chatbot_response = chatbot_interaction(user_input)
        return jsonify({'message': chatbot_response})

@app.route('/query_database', methods=['POST'])
def query_database():
    data = request.json
    model = data.get('model', '')
    year = data.get('year', '')
    
    car_review, num_car_reviews = get_car_review(year, model)

    if car_review is not None:
        return jsonify({'message': f"Found {num_car_reviews} reviews for {year} {model}: {car_review}"})
    else:
        return jsonify({'message': f"No reviews found for {year} {model}"})

if __name__ == "__main__":
    app.run(debug=True)
