const API_BASE_URL = window.location.origin;

const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Stops the '?' refresh in the URL

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login Success!");
                window.location.href = 'dashboard.html';
                // Add this inside your login success logic in auth.js
                localStorage.setItem("user_id", data.user_id); 
                localStorage.setItem("username", data.username);
            } else if (response.status === 401) {
                alert("Invalid email or password. Please try again.");
            } else {
                alert("Error: " + (data.message || "Unknown error occurred"));
            }
        } catch (error) {
            console.error("Connection failed:", error);
            alert("Server unreachable. Ensure your Flask app is running!");
        }
    });
}