function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    displayUserMessage(userInput);
    // Call backend API to get bot response
    // Replace the setTimeout with your actual API call
    setTimeout(function() {
        var botResponse = "This is a bot response. Replace it with actual response.";
        displayBotMessage(botResponse);
        displayGeneratedText(botResponse);
    }, 1000);
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

function displayGeneratedText(text) {
    var generatedTextContainer = document.getElementById('generated-text-container');
    var generatedTextDiv = document.createElement('div');
    generatedTextDiv.className = 'bot-message';
    generatedTextDiv.textContent = text;
    generatedTextContainer.appendChild(generatedTextDiv);
}
