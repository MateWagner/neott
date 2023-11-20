const WAIT_TO_RESPONSE = 3;

function arriveEvent(socket, topic) {
  socket.on(String(`${topic}/state`), (data) => {
    const item = document.getElementById(String(topic));
    item.value = data;
    removeTimer(item);
    setServerStateAttribute(item, data);
  });
}

function removeTimer(item) {
  if (item.hasAttribute("data-timer-id")) {
    clearTimeout(item.getAttribute("data-timer-id"));
    item.removeAttribute("data-timer-id");
  }
}

function setServerStateAttribute(item, data) {
  item.setAttribute("data-server-state", data);
}

function resetValue(item) {
  item.value = item.getAttribute("data-server-state");
  removeTimer(item);
  addAlert();
}

function resetChecked(item) {
  const serverState = item.getAttribute("data-server-state") === "ON";
  changeMainSwitchIcon(serverState);
  item.checked = serverState;
  addAlert();
  removeTimer(item);
}

function addAlert() {
  const alertRootDiv = document.getElementById("alert");
  const alert = document.createElement("div");
  alert.classList.add("alert");
  alert.classList.add("alert-danger");
  alert.classList.add("alert-dismissible");
  alert.role = "alert";
  alert.innerText = `Server time out: ${WAIT_TO_RESPONSE}s`;
  const close = document.createElement("button");
  close.classList.add("btn-close");
  close.setAttribute("data-bs-dismiss", "alert");
  close.setAttribute("aria-label", "Close");
  close.addEventListener("click", () => (alertRootDiv.innerHTML = ""));
  alert.appendChild(close);
  alertRootDiv.appendChild(alert);
}

function fallBackTimer(item, callback) {
  return setTimeout(() => callback(item), WAIT_TO_RESPONSE * 1000);
}

// Event listener for sending messages to the server
function returnData(socket, event) {
  const item = event.target;
  const topicName = item.id;
  const value = isNaN(item.value) ? item.value : Number(item.value);
  socket.emit(topicName, value);
  const timeoutId = fallBackTimer(item, resetValue);
  item.setAttribute("data-timer-id", timeoutId);
}

function returnEvent(socket, topic) {
  const item = document.getElementById(String(topic));
  item.addEventListener("change", (e) => returnData(socket, e));
}

function handleMainSwitch(socket) {
  const mainSwitch = document.getElementById("main_switch");
  mainSwitch.addEventListener("change", (event) => {
    const item = event.target;
    const switchState = item.checked ? "ON" : "OFF";
    changeMainSwitchIcon(item.checked);
    socket.emit("main_switch", switchState);
    const timeoutId = fallBackTimer(item, resetChecked);
    item.setAttribute("data-timer-id", timeoutId);
  });
  socket.on("main_switch/state", (data) => {
    mainSwitch.checked = data === "ON";
    changeMainSwitchIcon(data === "ON");
    removeTimer(mainSwitch);
    setServerStateAttribute(mainSwitch, data);
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
        return;
      }
      setTheme(false);
    });
}

function getSystemTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function changeMainSwitchIcon(isOn) {
  const onIcon = document.getElementById("main-swich-on");
  const offIcon = document.getElementById("main-swich-off");
  if (isOn) {
    onIcon.style.display = "inline";
    offIcon.style.display = "none";
    return;
  }
  offIcon.style.display = "inline";
  onIcon.style.display = "none";
}

function showTypeFactory(socket) {
  socket.on("show_type/list", createAndAddOptions);
}

function createAndAddOptions(showTypeList) {
  select_element = document.getElementById("show_type");
  select_element.innerHTML = "";

  for (key of Object.keys(showTypeList)) {
    option = document.createElement("option");
    option.label = showTypeList[key];
    option.value = key;
    select_element.appendChild(option);
  }
}

function init() {
  const socket = io();
  setTheme(getSystemTheme());
  handleThemeChange();
  handleMainSwitch(socket);
  showTypeFactory(socket);
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
