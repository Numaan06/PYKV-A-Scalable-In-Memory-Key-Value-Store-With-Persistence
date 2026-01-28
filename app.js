const BASE = "http://127.0.0.1:8000";

const getToken = () => localStorage.getItem("token");
const logout = () => { 
    localStorage.removeItem("token"); 
    window.location.href = "login.html"; 
};

// --- 1. REGISTRATION ---
async function registerUser() {
    const u = document.getElementById("ruser").value;
    const p = document.getElementById("rpass").value;

    if (!u || !p) return alert("Please fill all fields");

    try {
        const res = await fetch(`${BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: u, password: p })
        });

        if (res.ok) {
            alert("Registration Successful!");
            window.location.href = "login.html";
        } else {
            const err = await res.json();
            alert("Error: " + (err.detail || "Registration failed"));
        }
    } catch (e) {
        alert("Server error. Check if backend is running.");
    }
}

// --- 2. LOGIN ---
async function loginUser() {
    const u = document.getElementById("luser").value;
    const p = document.getElementById("lpass").value;

    const formData = new URLSearchParams();
    formData.append("username", u);
    formData.append("password", p);

    try {
        const res = await fetch(`${BASE}/login`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        if (res.ok && data.access_token) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "dashboard.html";
        } else {
            alert("Login Failed: Check your username/password");
        }
    } catch (e) {
        alert("Server connection failed");
    }
}

// --- 3. DASHBOARD LOGIC ---
async function refreshTable() {
    try {
        const res = await fetch(`${BASE}/list`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const data = await res.json();
        const tableBody = document.getElementById("dataTable");
        if (tableBody) {
            tableBody.innerHTML = "";
            for (const [key, value] of Object.entries(data)) {
                tableBody.innerHTML += `<tr><td><b>${key}</b></td><td>${value}</td></tr>`;
            }
        }
    } catch (e) { console.log("Dashboard list fetch failed"); }
}

async function setStoreValue() {
    const k = document.getElementById("setKey").value;
    const v = document.getElementById("setVal").value;
    const res = await fetch(`${BASE}/set`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ key: k, value: v })
    });
    if (res.ok) {
        document.getElementById("setKey").value = "";
        document.getElementById("setVal").value = "";
        refreshTable();
    }
}

async function getStoreValue() {
    const k = document.getElementById("getKey").value;
    const display = document.getElementById("getResult");
    const res = await fetch(`${BASE}/get/${k}`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    const data = await res.json();
    display.innerText = res.ok ? `Value: ${data.value}` : "Not found";
}

async function deleteStoreValue() {
    const k = document.getElementById("delKey").value;
    const res = await fetch(`${BASE}/delete/${k}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    if (res.ok) {
        alert("Deleted!");
        refreshTable();
    }
}

// --- 4. THE INITIALIZER (Connects Buttons to Functions) ---
window.onload = () => {
    // Connect Register Page
    const rb = document.getElementById("regBtn");
    if (rb) rb.onclick = registerUser;

    // Connect Login Page
    const lb = document.getElementById("loginBtn");
    if (lb) lb.onclick = loginUser;

    // Connect Dashboard Buttons
    const sb = document.getElementById("btnSet");
    const gb = document.getElementById("btnGet");
    const db = document.getElementById("btnDel");

    if (sb) {
        sb.onclick = setStoreValue;
        gb.onclick = getStoreValue;
        db.onclick = deleteStoreValue;
        refreshTable(); 
    }
};