const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const userName = document.getElementById('user-name');
const agentName = document.getElementById('agent-name');

let participants = [
  { name: "You", id: "user" },
  { name: "AI Agent", id: "agent" }
];

let isFirstClick = true;

function addMessage(content, isUser) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message');
  messageDiv.classList.add(isUser ? 'user-message' : 'agent-message');
  messageDiv.textContent = content;
  messageDiv.setAttribute('data-sender', isUser ? participants[0].name : participants[1].name);
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function clearMessages() {
  chatMessages.innerHTML = '';
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (message) {
    userInput.value = '';

    if (message.toLowerCase() === 'clear') {
      clearMessages();
    } else {
      addMessage(message, true);
      // Simulate AI response (replace with actual API call in a real scenario)
      const response = await simulateAIResponse(message);
      addMessage(response, false);
    }
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

function updateTableParticipants(user, agent) {
    const userName = document.getElementById('user-name');
    const agentName = document.getElementById('agent-name');
    userName.textContent = user;
    agentName.textContent = agent;
    document.getElementById('table-participant1').textContent = user;
    document.getElementById('table-participant2').textContent = agent;
    document.getElementById('h1-other').textContent = `→ ${agent}`;
    document.getElementById('h2-other').textContent = `→ ${user}`;
}

function changeName(element, participantIndex) {
    const newName = prompt(`Enter name for ${participants[participantIndex].name}:`);
    if (newName && newName.trim()) {
        element.textContent = newName.trim();
        participants[participantIndex].name = newName.trim();
        updateTableParticipants(participants[0].name, participants[1].name);
    }
}

function updateParticipantsUI() {
    const user = document.getElementById('user-name').textContent;
    const agent = document.getElementById('agent-name').textContent;
    document.getElementById('table-participant1').textContent = user;
    document.getElementById('table-participant2').textContent = agent;
    document.getElementById('h1-other').textContent = `→ ${agent}`;
    document.getElementById('h2-other').textContent = `→ ${user}`;
}

document.body.addEventListener("htmx:trigger", (evt) => {
    if (evt.detail.name === "participants-updated") {
        updateParticipantsUI();
    }
});

clickCount = 0
// Update this event listener
document.getElementById('next-line').addEventListener('click', function() {
    if (this.textContent === 'conv-1') {
        if (clickCount === 0) {
            document.getElementById('chat-messages').innerHTML = '';
            clickCount++;
        } else if (clickCount === 1) {
            updateParticipantsUI();
        }
    }
});

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

userName.addEventListener('click', () => changeName(userName, 0));
agentName.addEventListener('click', () => changeName(agentName, 1));

document.addEventListener('analyze-conversation', () => {
    console.log("analyze-conversation event triggered");
});
