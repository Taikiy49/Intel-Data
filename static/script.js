// script.js

function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    displayUserMessage(userInput);

    // Send AJAX request to Flask server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_bot_response', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            displayBotMessage(response.bot_response);
        }
    };
    xhr.send('user_input=' + userInput);
}

function displayUserMessage(message) {
    var chatMessages = document.getElementById('chat-messages');
    var userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.textContent = message;
    chatMessages.appendChild(userMessageDiv);
    document.getElementById('user-input').value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayBotMessage(message) {
    var chatMessages = document.getElementById('chat-messages');
    var botMessageDiv = document.createElement('div');
    botMessageDiv.className = 'bot-message';
    botMessageDiv.textContent = message;
    chatMessages.appendChild(botMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
