document.addEventListener("DOMContentLoaded", function() {
    var chatLog = document.getElementById("chatLog");
    var userInput = document.getElementById("userInput");
    var sendBtn = document.getElementById("sendBtn");

    sendBtn.addEventListener("click", function() {
        var userMessage = userInput.value.trim();
        if (userMessage !== "") {
            appendMessage("You: " + userMessage, "user");

            // Make an AJAX request to the server with user's message
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/get_response", true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

            xhr.onload = function () {
                if (xhr.status >= 200 && xhr.status < 300) {
                    var botResponse = JSON.parse(xhr.responseText).response;
                    appendMessage("Bot: " + botResponse, "bot");
                }
            };

            var data = JSON.stringify({ "message": userMessage });
            xhr.send(data);

            userInput.value = "";
        }
    });

    function appendMessage(message, sender) {
        var messageWrapper = document.createElement("div");
        messageWrapper.classList.add("message", sender);
        messageWrapper.textContent = message;
        chatLog.appendChild(messageWrapper);
        // Scroll to the bottom of the chat log
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});
