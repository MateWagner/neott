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

function handleMainSwitch(socket) {
  const mainSwitch = document.getElementById("main_switch");
  mainSwitch.addEventListener("change", (e) => {
    const switchState = e.target.checked ? "ON" : "OFF";
    changeMainSwichIcon(e.target.checked)
    socket.emit("main_switch", switchState);
  });
  socket.on("main_switch", (data) => {
    mainSwitch.checked = data === "ON";
    changeMainSwichIcon(data === "ON")
  });
}

function setTheme(isDark) {
  const body = document.getElementsByTagName("body")[0];
  body.setAttribute("data-bs-theme", isDark ? "dark" : "light");
}

function handleThemeChange() {
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", ({ matches }) => {
      if (matches) {
        setTheme(true);
      } else {
        setTheme(false);
      }
    });
}

function getSystemTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function changeMainSwichIcon(isOn) {
  const onIcon = document.getElementById('main-swich-on')
  const offIcon = document.getElementById('main-swich-off')
  if(isOn){
    onIcon.style.display = 'inline'
    offIcon.style.display = 'none'
    return
  }
  offIcon.style.display = 'inline'
  onIcon.style.display = 'none'
}

function init() {
  const socket = io();
  setTheme(getSystemTheme());
  handleThemeChange();
  handleMainSwitch(socket);
  const topics = {
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
