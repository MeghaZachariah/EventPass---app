fetch("http://127.0.0.1:5000/get_events")
.then(res => res.json())
.then(data => {
    const container = document.getElementById("events");

    container.innerHTML = "";

    data.forEach(event => {
    container.innerHTML += `
        <div class="event-card" onclick="viewEvent(${event.id}, '${event.title}')">
            <h3>${event.title}</h3>
            <div class="event-info">
                <span>📅 ${event.date}</span>
                <br>
                <span>📍 ${event.location}</span>
            </div>
        </div>
    `;
});
});

function viewEvent(id, title) {
    localStorage.setItem("event_id", id);
    localStorage.setItem("event_title", title);
    window.location.href = "event.html";
}