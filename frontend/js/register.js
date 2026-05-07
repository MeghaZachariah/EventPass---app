// frontend/js/register.js

async function handleRegistration() {
    const userId = localStorage.getItem('user_id');
    // Ensure the key matches what you saved when clicking 'Get Details'
    const selectedEvent = JSON.parse(localStorage.getItem('selectedEvent'));

    if (!userId || !selectedEvent) {
        alert("Please log in to register.");
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/register_event', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                event_id: selectedEvent.id // Ensure your backend expects 'event_id'
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Registered! Your QR Pass is being generated.");
            window.location.href = 'qr.html';
        } else {
            alert(data.message || "Registration failed.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Server connection failed.");
    }
}

// Attach the function to your button
document.addEventListener('DOMContentLoaded', () => {
    const confirmBtn = document.getElementById('confirmBtn'); // Check your HTML for this ID
    if (confirmBtn) {
        confirmBtn.addEventListener('click', handleRegistration);
    }
});