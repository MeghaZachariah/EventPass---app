document.addEventListener("DOMContentLoaded", function() {
    const userId = localStorage.getItem("user_id");
    const username = localStorage.getItem("username");
    // Get the event ID from the last event the user clicked
    const eventId = localStorage.getItem("event_id"); 

    if (!userId || !eventId) {
        alert("Session expired or no event selected.");
        window.location.href = "dashboard.html";
        return;
    }

    document.getElementById("displayUsername").innerText = username;
    document.getElementById("displayUserId").innerText = `User: ${userId} | Event: ${eventId}`;

    // Path matches Person 3's logic: qr_{user_id}_{event_id}.png
    const qrImagePath = `../qr_module/qr_images/qr_${userId}_${eventId}.png`;
    
    const qrImgElement = document.getElementById("qrImage");
    qrImgElement.src = qrImagePath;

    qrImgElement.onerror = function() {
        this.src = "https://via.placeholder.com/200?text=QR+Not+Generated+Yet";
        console.warn("Looking for QR at: " + qrImagePath);
    };
});