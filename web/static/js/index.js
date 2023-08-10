function arriveEvent(socket, topic) {
  socket.on(String(topic), (data) => {
    const item = document.getElementById(String(topic));
    item.value = data;
  });
}

// Event listener for sending messages to the server
function returnData(socket, event) {
  const topicName = event.target.id;
  const value = isNaN(event.target.value)
    ? event.target.value
    : Number(event.target.value);
  socket.emit(topicName, value);
}

function returnEvent(socket, topic) {
  const item = document.getElementById(String(topic));
  item.addEventListener("change", (e) => returnData(socket, e));
}

function init() {
  const socket = io();
  const topics = {
    main_switch: "main_switch",
    hex_rgb: "hex_rgb",
    show_type: "show_type",
    wait: "wait",
    brightness: "brightness",
  };
  for (const topic of Object.values(topics)) {
    returnEvent(socket, topic);
    arriveEvent(socket, topic);
  }
}

init();
