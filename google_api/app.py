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
def get_car_reviews(year, word):
    car_reviews = car_reviews_dataset["train"].filter(lambda example: 'Toyota' in example["Vehicle_Title"] and year in example["Vehicle_Title"].split()[:] and (word in example["Review"].split()[:] or word.capitalize() in example["Review"].split()[:]))
    reviews = []
    for review in car_reviews:
        reviews.append(review["Review"])
    return reviews


# Function to handle regular chatbot interactions
def chatbot_interaction(user_input):
    convo = model.start_chat(history=[])
    convo.send_message(user_input)
    return convo.last.text

# Route to summarize the reviews
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key for Google Generative AI
genai.configure(api_key="YOUR_API_KEY")

# Set up the model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

@app.route('/summarize_reviews', methods=['POST'])
def summarize_reviews():
    # Extract reviews from the request
    data = request.json
    reviews = data.get('reviews', [])

    # Concatenate the reviews into a single string
    reviews_text = '\n'.join(reviews)

    # Append the prompt for summarization
    prompt = f"{reviews_text}\n\nsummarize for me"

    # Generate summary using Gemini AI
    summary = model.start_chat(history=[]).send_message(prompt).last.text

    return jsonify({'message': summary})


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
    
    car_reviews = get_car_reviews(year, model)

    if car_reviews:
        num_car_reviews = len(car_reviews)
        return jsonify({'message': f"Found {num_car_reviews} reviews for {year} {model}: {', '.join(car_reviews)}"})
    else:
        return jsonify({'message': f"No reviews found for {year} {model}"})


if __name__ == "__main__":
    app.run(debug=True)
