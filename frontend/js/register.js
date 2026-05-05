const eventId = localStorage.getItem("event_id");

const events = {
    1: "Tech Fest",
    2: "Music Night",
    3: "Sports Meet"
};

// show event name
document.getElementById("eventName").innerText = events[eventId];

// register button
function registerEvent() {
    alert("Registered for " + events[eventId]);
}