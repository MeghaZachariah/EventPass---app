// register.js
document.addEventListener("DOMContentLoaded", () => {
    const confirmBtn = document.getElementById('confirmBtn');

    if (confirmBtn) {
        confirmBtn.addEventListener('click', async (e) => {
            e.preventDefault(); // Prevents any accidental page reloads
            
            // Get data from localStorage saved during login
            const userId = localStorage.getItem("user_id");
            const eventId = "1"; // Default for your Python Workshop

            try {
                const response = await fetch(`${window.location.origin}/register_event`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        user_id: userId, 
                        event_id: eventId 
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Registration Confirmed!");
                    // Redirect to the QR page
                    window.location.href = `qr.html?user_id=${userId}&event_id=${eventId}`;
                } else {
                    alert("Error: " + data.message);
                }
            } catch (error) {
                console.error("Fetch error:", error);
                alert("Cannot connect to server. Check your terminal.");
            }
        });
    } else {
        console.error("Button with ID 'confirmBtn' not found!");
    }
});