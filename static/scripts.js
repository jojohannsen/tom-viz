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

    if (message.toLowerCase().startsWith('load')) {
      const filename = message.split(' ')[1];
      if (filename) {
        try {
          const response = await axios.get(`/load?filename=${encodeURIComponent(filename)}`);
          if (!response.data.content) {
            throw new Error("File not found");
          }
          addMessage(`File ${filename} loaded successfully.`, false);
          // Process the response content
          const lines = response.data.content.split('\n');
          const extractedNames = extractParticipantNames(lines);
          if (extractedNames.length === 2) {
            addMessage(`Extracted participants: ${extractedNames[0]} and ${extractedNames[1]}`, false);
            participants[0].name = extractedNames[0];
            participants[1].name = extractedNames[1];
            updateTableParticipants();
          } else {
            addMessage("Couldn't find two participant names in the file.", false);
          }
        } catch (error) {
          addMessage(`Error loading file ${filename}: ${error.response?.data || error.message}`, false);
        }
      } else {
        addMessage("Please specify a filename to load.", false);
      }
    } else {
      // Simulate AI response (replace with actual API call in a real scenario)
      const response = await simulateAIResponse(message);
      addMessage(response, false);
    }
  }
}

function extractParticipantNames(lines) {
  const names = [];
  for (const line of lines) {
    const trimmedLine = line.trim();
    const name = line.split(':')[0]

    if (!names.includes(name)) {
        names.push(name);
        if (names.length === 2) {
          break;
        }
    }
  }
  return names;
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
    const userName = document.getElementById('user-name');
    const agentName = document.getElementById('agent-name');
    userName.textContent = participants[0].name;
    agentName.textContent = participants[1].name;
    document.getElementById('table-participant1').textContent = participants[0].name;
    document.getElementById('table-participant2').textContent = participants[1].name;
    document.getElementById('h1-other').textContent = `→ ${participants[1].name}`;
    document.getElementById('h2-other').textContent = `→ ${participants[0].name}`;
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
