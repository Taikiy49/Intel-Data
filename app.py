from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    data = request.json  
    user_input = data['user_input']  # Input from html file
    # Process user input and generate bot response
    bot_response = "Bot response From Flask: " + user_input
    print(user_input)
    return jsonify({'bot_response': bot_response}) # Output to html

if __name__ == '__main__':
    app.run(debug=True)