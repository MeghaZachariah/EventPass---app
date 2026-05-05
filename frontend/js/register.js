function registerEvent() {
    const eventId = localStorage.getItem("event_id");
    const userId = localStorage.getItem("user_id");

    if (!eventId || !userId) {
        alert("Error: User or Event session missing. Please log in again.");
        window.location.href = "login.html";
        return;
    }

    fetch("http://127.0.0.1:5000/register_event", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json" 
        },
        body: JSON.stringify({ 
            event_id: eventId,
            user_id: userId 
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        
            if (data.message === "Registration successful!" || data.message === "Already registered!") {
                window.location.href = "dashboard.html";
            }
        } else if (data.error) {
            alert("Error: " + data.error);
        }
    })
    .catch(err => {
        console.error("Fetch error:", err);
        alert("Server connection failed. Make sure the backend is running.");
    });
}