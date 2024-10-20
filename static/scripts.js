const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const userName = document.getElementById('user-name');
const agentName = document.getElementById('agent-name');

let participants = [
  { name: "You", id: "user" },
  { name: "AI Agent", id: "agent" }
];

function addMessage(content, isUser) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message');
  messageDiv.classList.add(isUser ? 'user-message' : 'agent-message');
  messageDiv.textContent = content;
  messageDiv.setAttribute('data-sender', isUser ? participants[0].name : participants[1].name);
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (message) {
    addMessage(message, true);
    userInput.value = '';

    // Simulate AI response (replace with actual API call in a real scenario)
    const response = await simulateAIResponse(message);
    addMessage(response, false);
  }
}

async function simulateAIResponse(message) {
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate delay
  const responses = [
    "That's an interesting point. Can you tell me more?",
    "I understand. How does that make you feel?",
    "Thank you for sharing. Is there anything else on your mind?",
    "I see. What do you think we should do about that?",
    "That's a great question. Let me think about it for a moment."
  ];
  return responses[Math.floor(Math.random() * responses.length)];
}

function updateTableParticipants() {
    document.getElementById('table-participant1').textContent = participants[0].name;
    document.getElementById('table-participant2').textContent = participants[1].name;
}

// Call this function initially to set the names
updateTableParticipants();

function changeName(element, participantIndex) {
    const newName = prompt(`Enter name for ${participants[participantIndex].name}:`);
    if (newName && newName.trim()) {
        element.textContent = newName.trim();
        participants[participantIndex].name = newName.trim();
        updateTableParticipants(); // Update the table when names change
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

userName.addEventListener('click', () => changeName(userName, 0));
agentName.addEventListener('click', () => changeName(agentName, 1));
