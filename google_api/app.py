from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from datasets import load_dataset

app = Flask(__name__)

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyApdIIDxko0YfMZ_xMatRdFSfXN2eaY8WI")
"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

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

prompt_parts = [
  "input: Why do you exist?",
  "output: To explain to you more about Toyota cars.",
  "input: Why are you here?",
  "output: To explain to you more about Toyota cars.",
  "input: What do you do here?",
  "output: To explain to you more about Toyota cars.",
  "input: What are you an expert in?",
  "output: To explain to you more about Toyota cars.",
  "input: Will you talk about other stuff?",
  "output: I will only talk to you about Toyota cars.",
  "input: Will you talk about other stuff?",
  "output: As I've said I will only talk about Toyota cars.",
  "input: Tell me more about other cars.",
  "output: No, I will only talk about Toyota cars if that's what you are trying to figure.",
  "input: Please talk nicely to everyone",
  "output: Understood. Apologies!",
  "input: Should I buy a Toyota?",
  "output: Yes! Definitely!",
  "input: What am I supposed to do in the sections above?",
  "output: In the section above you can look for reviews that thousands of our customers have left in the past!",
  "input: What am I supposed to do here?",
  "output: You can find reviews of the specific Toyota car you are looking for!",
  "input: cart = {} initially.\nif user adds a 2012 corolla, cart = {2012:[corolla]}\nif user adds a 2012 camry on top of that, cart = {2012:[corolla, camry]\nif user adds a 2014 camry on top of that, cart = {2012: [corolla, camry], 2014: [camry]}",
  "output: cart = {2012: [corolla, camry], 2014: [camry]}",
  "input: What will you only talk about?",
  "output: Toyota",
  "input: Will you give information about other companies besides Toyota?",
  "output: No, I will only talk about Toyota.",
  "input: Will you be nice to customers?",
  "output: I will be extremely nice and polite to customers.",
  "input: Will you advertise or talk about stuff unrelated to Toyota even if they ask you?",
  "output: No.",
  "input: You will not talk about anything other than Toyota",
  "output: I will not talk about ANYTHING other than Toyota.",
  "input: What will you do if someone asks a question that isn't about Toyota?",
  "output: You will tell them that you are only able to answer Toyota-related questions.",
  "input: Also please do not use bold letters or anything in your responses keep everything in normal standard text.",
  "output: Agreed. I will not bold letters or change any formatting in my responses.",
  "input: Do not respond to anything other than Toyota-related questions.",
  "output: I will not respond to anything other than Toyota-related questions.",
  "input: What do you do in this UI?",
  "output: The UI will assist you through sorting and analyzing reviews from tens and thousands of past customers!",
]
# idk why this is not working but!!!
response = model.generate_content(prompt_parts)

car_reviews_dataset = load_dataset("florentgbelidji/car-reviews")

# Helper function to query the database
def get_car_reviews(year, model, word):
    car_reviews = car_reviews_dataset["train"].filter(lambda example: 'Toyota' in example["Vehicle_Title"] and year in example["Vehicle_Title"].split()[:] and (model in example["Vehicle_Title"] and (word in example["Review"].split()[:] or word.capitalize() in example["Review"].split()[:])))
    reviews = []
    for review in car_reviews:
        reviews.append(review["Review"])
    return reviews

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
    count = 0
    data = request.json
    model = data.get('model', '')
    year = data.get('year', '')
    word = data.get('word', '')

    car_reviews = get_car_reviews(year, model, word)

    if car_reviews:
        return jsonify({'message': f"{', '.join(car_reviews)}"})
    else:
        return jsonify({'message': f"No reviews found for {year} {model}"})

@app.route('/summarize_reviews', methods=['POST'])
def summarize_reviews():
    data = request.json
    reviews = data.get('reviews', [])
    reviews_text = '\n'.join(reviews)
    chatbot_summary = chatbot_interaction(f"{reviews_text}\n\nsummarize for me in simple words")
    return jsonify({'message': chatbot_summary})

@app.route('/positive_reviews', methods=['POST'])
def positive_reviews():
    data = request.json
    reviews = data.get('reviews', [])
    reviews_text = '\n'.join(reviews)
    chatbot_summary = chatbot_interaction(f"{reviews_text}\n\nFind me all of the positive reviews and leave out all the negative reviews.")
    return jsonify({'message': chatbot_summary})

@app.route('/negative_reviews', methods=['POST'])
def negative_reviews():
    data = request.json
    reviews = data.get('reviews', [])
    reviews_text = '\n'.join(reviews)
    chatbot_summary = chatbot_interaction(f"{reviews_text}\n\nFind me all of the negative reviews and leave out all of the positive reviews.")
    return jsonify({'message': chatbot_summary})
    
if __name__ == "__main__":
    app.run(debug=True)
