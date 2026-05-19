// frontend/js/auth.js

document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. LOGIN HANDLING LOGIC
    // ==========================================
    const loginForm = document.getElementById('loginForm');
    const btnParticipant = document.getElementById('btn-participant');
    const btnOrganizer = document.getElementById('btn-organizer');
    
    // Track the currently selected login role (defaults to participant matching login.html)
    let currentLoginRole = 'participant';

    // Toggle Visual Selection Design Styles for Login Tabs
    if (btnParticipant && btnOrganizer) {
        btnParticipant.addEventListener('click', () => {
            currentLoginRole = 'participant';
            
            // Set active participant button appearance
            btnParticipant.className = "w-1/2 bg-white text-[#0B1E3F] py-2.5 rounded-xl text-sm font-bold shadow-sm transition-all";
            // Dim organizer button appearance
            btnOrganizer.className = "w-1/2 text-slate-400 py-2.5 rounded-xl text-sm font-medium transition-all";
        });

        btnOrganizer.addEventListener('click', () => {
            currentLoginRole = 'organizer';
            
            // Set active organizer button appearance
            btnOrganizer.className = "w-1/2 bg-white text-[#0B1E3F] py-2.5 rounded-xl text-sm font-bold shadow-sm transition-all";
            // Dim participant button appearance
            btnParticipant.className = "w-1/2 text-slate-400 py-2.5 rounded-xl text-sm font-medium transition-all";
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const emailInput = document.getElementById('loginEmail');
            const passwordInput = document.getElementById('loginPassword');

            if (!emailInput.value || !passwordInput.value) {
                alert("Please enter both your email and password.");
                return;
            }

            const loginPayload = {
                Email: emailInput.value,
                Password: passwordInput.value,
                Role: currentLoginRole // Correctly forwards 'participant' or 'organizer'
            };

            console.log("Submitting login sequence payload:", loginPayload);

            try {
                const response = await fetch('http://127.0.0.1:5000/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(loginPayload)
                });

                const result = await response.json();

                if (response.ok) {
                    // Storing identity data strings securely across the browser environment
                    localStorage.setItem('user_id', result.User_ID);
                    localStorage.setItem('username', result.username);
                    localStorage.setItem('role', result.Role);

                    alert(`Welcome back, ${result.username}!`);
                    
                    // Route users out to the correct dashboard views matching their roles
                    if (result.Role === 'organizer') {
                        window.location.href = 'organizer.html';
                    } else {
                        window.location.href = 'dashboard.html';
                    }
                } else {
                    // This catches the "Invalid Email or Password" or account role mapping mismatch alerts
                    alert(result.message || "Login authentication failed.");
                }
            } catch (err) {
                console.error("Connection tracking error:", err);
                alert("Unable to communicate with authentication server engine.");
            }
        });
    }

    // ==========================================
    // 2. SIGNUP HANDLING LOGIC
    // ==========================================
    const signupForm = document.getElementById('signupForm') || document.querySelector('form:not(#loginForm)');
    
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const nameInput = document.getElementById('name') || document.querySelector('input[placeholder="Full Name"]') || document.querySelectorAll('input')[0];
            const emailInput = document.getElementById('email') || document.querySelector('input[placeholder="Email Address"]') || document.querySelectorAll('input')[1];
            const passwordInput = document.getElementById('password') || document.querySelector('input[placeholder="Password"]') || document.querySelectorAll('input')[2];
            
            let selectedRole = 'participant';
            const organizerTab = document.getElementById('organizerTab') || Array.from(document.querySelectorAll('button, span')).find(el => el.textContent.includes('Organizer'));
            
            if (organizerTab) {
                if (organizerTab.classList.contains('bg-white') || organizerTab.classList.contains('text-blue-600') || organizerTab.getAttribute('data-active') === 'true') {
                    selectedRole = 'organizer';
                }
            }

            if (!nameInput.value || !emailInput.value || !passwordInput.value) {
                alert("Please fill in all input credentials.");
                return;
            }

            const payload = {
                Name: nameInput.value,
                Email: emailInput.value,
                Password: passwordInput.value,
                Role: selectedRole
            };

            console.log("Sending registration payload parameters:", payload);

            try {
                const response = await fetch('http://127.0.0.1:5000/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (response.ok) {
                    alert("Account created successfully! Proceeding to authentication page.");
                    window.location.href = 'login.html';
                } else {
                    alert(result.message || "Registration failed.");
                }
            } catch (err) {
                console.error("Connection link offline:", err);
                alert("Could not reach authentication server.");
            }
        });
    }
});