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
    # Process user input and generate bot response
    convo = model.start_chat(history=[])
    convo.send_message(user_input)
    bot_response = convo.last.text
    print(user_input)
    return jsonify({'bot_response': bot_response}) # Output to html

if __name__ == '__main__':
    app.run(debug=True)
