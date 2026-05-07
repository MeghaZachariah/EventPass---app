document.addEventListener('DOMContentLoaded', () => {
    // 1. Handle Signup
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const selectedRole = document.querySelector('input[name="role"]:checked')?.value || 'participant';

    // MATCH THESE KEYS EXACTLY TO YOUR SQL SCHEMA
    const userData = {
        Name: document.getElementById('name').value,
        Email: document.getElementById('email').value,
        Password: document.getElementById('password').value,
        Role: selectedRole // This helps your backend route to ORGANIZER or PARTICIPANT tables
    };

    console.log("Sending data:", userData); // Helpful for debugging in F12 console

    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        

                const data = await response.json();

                if (response.ok) {
                    alert("Account created successfully!");
                    window.location.href = 'login.html';
                } else {
                    // This will show the SQLite error if something goes wrong
                    alert("Error: " + (data.message || "Signup failed"));
                }
            } catch (error) {
                console.error("Signup error:", error);
                alert("Cannot connect to server. Ensure Flask is running.");
            }
        });
    }

    // 2. Handle Login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const loginData = {
                Email: document.getElementById('email').value,
                Password: document.getElementById('password').value
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(loginData)
                });

                const data = await response.json();

                if (response.ok) {
                    // Storing session data
                    localStorage.setItem('user_id', data.User_ID); 
                    localStorage.setItem('username', data.Name);
                    localStorage.setItem('role', data.Role);

                    if (data.Role === 'organizer') {
                        window.location.href = 'organizer.html';
                    } else {
                        window.location.href = 'dashboard.html';
                    }
                } else {
                    alert(data.message || "Invalid Email or Password.");
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("Login failed. Check backend logs.");
            }
        });
    }
});