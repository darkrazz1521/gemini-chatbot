// ================================
// Get HTML Elements
// ================================
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const loading = document.getElementById("loading");

// ================================
// Add Message to Chat
// ================================
function addMessage(message, sender) {

    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    bubble.textContent = message;

    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);

    // Auto Scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ================================
// Send Message to Flask
// ================================
async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    // Show User Message
    addMessage(message, "user");

    // Clear Input
    input.value = "";

    // Show Loading
    loading.classList.remove("hidden");

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        // Hide Loading
        loading.classList.add("hidden");

        // Show Gemini Reply
        addMessage(data.reply, "bot");

    }

    catch (error) {

        loading.classList.add("hidden");

        addMessage(
            "Something went wrong. Please try again.",
            "bot"
        );

        console.error(error);

    }

}

// ================================
// Button Click
// ================================
sendBtn.addEventListener("click", sendMessage);

// ================================
// Press Enter to Send
// Shift + Enter = New Line
// ================================
input.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});