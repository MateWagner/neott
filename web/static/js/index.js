const socket = io(); // This creates a WebSocket connection to the server
const topics = {
  main_switch: "main_switch",
  solid_color: "solid_color",
  show_type: "show_type",
  wait: "wait",
  brightness: "brightness",
};
// Event listener for receiving messages from the server
socket.on("message", (data) => {
  const messagesDiv = document.getElementById("messages");
  messagesDiv.innerHTML += `<p>${data}</p>`;
});

socket.on(topics.brightness, (data) => {
  const brightness = document.getElementById("brightness");
  brightness.value = data;
});

socket.on(topics.wait, (data) => {
  const wait = document.getElementById("wait");
  wait.value = data;
});

// Event listener for sending messages to the server
function sendMessage() {
  const message = prompt("Enter your message:");
  socket.emit("message", message);
}

function returnData(event) {
  const topicName = event.target.id;
  const value = isNaN(event.target.value)
    ? event.target.value
    : Number(event.target.value);
  socket.emit("return-data", JSON.stringify({ [topicName]: value }));
}

function subscribeToEvents(topic) {
  const item = document.getElementById(String(topic));
  item.addEventListener("change", returnData);
}

function init() {
  for (const topic of Object.values(topics)) {
    console.log(topic);
    subscribeToEvents(topic);
  }
}

init();
