document.getElementById("eventForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const eventData = {
        title: document.getElementById("title").value,
        date: document.getElementById("date").value,
        location: document.getElementById("location").value,
        capacity: document.getElementById("capacity").value
    };

    fetch("http://127.0.0.1:5000/create_event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = "dashboard.html";
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(err => alert("Failed to create event. Check server connection."));
});