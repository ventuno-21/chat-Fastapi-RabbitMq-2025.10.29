const BACKEND_URL = CONFIG.BACKEND_URL;


// -----------------------------
// Login Function
// -----------------------------
async function login(username, password) {
    const res = await fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
        alert("Login failed!");
        return null;
    }

    const data = await res.json();
    // Save JWT to localStorage
    localStorage.setItem("jwt_token", data.access_token);
    return data.access_token;
}

// -----------------------------
// Send Message
// -----------------------------
document.getElementById("message-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const input = document.getElementById("message-input");
    const content = input.value;
    if (!content) return;

    // Replace with actual receiver/group/channel ID
    const payload = {
        content,
        receiver_id: 2,
        self_destruct: false,
    };

    // Get JWT from localStorage
    const token = localStorage.getItem("jwt_token");
    if (!token) {
        alert("You must login first!");
        return;
    }

    const res = await fetch(`${BACKEND_URL}/chat/send`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token, // ✅ Header with JWT
        },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        alert("Failed to send message");
        return;
    }

    const data = await res.json();
    renderMessage(data);
    input.value = "";
});

// -----------------------------
// Render Message in Chat Box
// -----------------------------
function renderMessage(msg) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");

    if (msg.is_image && msg.file_base64) {
        const img = document.createElement("img");
        img.src = "data:image/jpeg;base64," + msg.file_base64;
        div.appendChild(img);
    }

    if (msg.content) {
        const p = document.createElement("p");
        p.textContent = msg.content;
        div.appendChild(p);
    }

    box.appendChild(div);
}

// -----------------------------
// Example Usage: Login on page load
// -----------------------------
document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const token = await login(username, password);
    if (token) {
        alert("Login successful!");
    }
});
