document.getElementById("signupForm")?.addEventListener("submit", function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, role })
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok) {
            alert("Signup successful!");
            window.location.href = "login.html";
        } else {
            alert("Signup failed: " + (data.error || "Unknown error"));
        }
    })
    .catch(err => {
        console.error(err);
        alert("Server error. Check if backend is running!");
    });
});

// --- LOGIN LOGIC ---
document.getElementById("loginForm")?.addEventListener("submit", function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(async res => {
        const data = await res.json();
        // Inside your auth.js login .then()
        if (res.ok) {
        alert("Login successful!");
        localStorage.setItem("username", data.username); 
        localStorage.setItem("user_id", data.user_id); // <--- ADD THIS LINE
        window.location.href = "dashboard.html";
        } else {
            alert("Login failed: " + (data.error || "Invalid Credentials"));
        }
    })
    .catch(err => {
        console.error(err);
        alert("Login failed. Make sure the server is on.");
    });
});