function sendMessage() {
    var userInput = document.getElementById('user-input').value;

    // Send AJAX request to Flask server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_bot_response', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            displayMessage(userInput, response.bot_response);
        }
    };
    xhr.send(JSON.stringify({ user_input: userInput }));
    document.getElementById('user-input').value = '';
}

function displayMessage(userInput, botResponse) {
    var messageHistory = document.getElementById('message-history');

    var userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.textContent = '[USER]: ' + userInput;
    messageHistory.appendChild(userMessageDiv);

    var botMessageDiv = document.createElement('div');
    botMessageDiv.className = 'bot-message';
    botMessageDiv.textContent = '[AI ASSISTANT]: ' + botResponse;
    messageHistory.appendChild(botMessageDiv);
}
