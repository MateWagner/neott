const socket = io(); // This creates a WebSocket connection to the server

// Event listener for receiving messages from the server
socket.on("message", (data) => {
  const messagesDiv = document.getElementById("messages");
  messagesDiv.innerHTML += `<p>${data}</p>`;
});

// Event listener for sending messages to the server
function sendMessage() {
  const message = prompt("Enter your message:");
  socket.emit("message", message);
}
