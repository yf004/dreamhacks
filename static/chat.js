const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const messagesArea = document.getElementById('messagesArea');

// Set initial height for the textarea
messageInput.style.height = '3.75rem'; // Initial size for one line

// Auto-resize textarea with maximum height limit
messageInput.addEventListener('input', function() {
  // Reset height to auto first to get accurate scroll height
  this.style.height = '3.75rem'; // Start with single line height
 
  // Only grow if content exceeds current height
  if (this.scrollHeight > this.clientHeight) {
    // Calculate new height with a maximum limit (4 lines approximately)
    const newHeight = Math.min(this.scrollHeight, 120);
   
    // Apply the new height in pixels for smoother transition
    this.style.height = newHeight + 'px';
  }
});

// Send message function
function sendMessage() {
  const message = messageInput.value.trim();
  if (message) {
    // Create user message bubble
    const userMessageBubble = document.createElement('div');
    userMessageBubble.className = 'message-bubble user-message';
    userMessageBubble.textContent = message;
   
    // Add to messages area
    messagesArea.appendChild(userMessageBubble);
   
    // Clear input and reset height
    messageInput.value = '';
    messageInput.style.height = '3.75rem';
   
    // Add AI response (after a small delay to simulate thinking)
    setTimeout(() => {
      // Create AI message bubble
      const aiMessageBubble = document.createElement('div');
      aiMessageBubble.className = 'message-bubble ai-message';
      aiMessageBubble.textContent = "[Insert AI response]";
   
      // Add to messages area
      messagesArea.appendChild(aiMessageBubble);
   
      // Scroll messages to bottom
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }, 500);
    
    // Scroll messages to bottom after user message
    messagesArea.scrollTop = messagesArea.scrollHeight;
  }
}

// Send button click
sendButton.addEventListener('click', sendMessage);

// Enter key to send (Shift+Enter for new line)
messageInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Back button functionality
document.querySelector('.back-button').addEventListener('click', function() {
  // You can add navigation logic here
  console.log('Back button clicked');
});