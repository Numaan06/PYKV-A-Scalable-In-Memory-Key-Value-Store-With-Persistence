# 🔐 PyKV Secure Store

PyKV is a modern, secure, and high-performance **Key-Value Storage System**. It features a beautiful "Glassmorphism" frontend and a robust FastAPI backend secured with **JWT (JSON Web Tokens)**.



---

## 🚀 Key Features

* **Secure Authentication:** User registration and login powered by OAuth2 and JWT.
* **CRUD Operations:** Effortlessly **Set**, **Get**, and **Delete** key-value pairs.
* **Real-time Dashboard:** A visual data table that updates instantly as you manage your records.
* **Modern UI:** A responsive, attractive interface built with CSS Glassmorphism and the Poppins font.
* **In-Memory Storage:** Fast data handling using Python dictionaries for high-speed performance.

---

## 🛠️ Tech Stack

### **Backend**
* **Python / FastAPI:** High-performance web framework for the API.
* **Jose (python-jose):** For JWT generation and verification.
* **Pydantic:** For data validation and settings management.
* **Uvicorn:** The lightning-fast ASGI server.

### **Frontend**
* **HTML5 & CSS3:** Modern layouts with custom animations and Glassmorphism effects.
* **Vanilla JavaScript:** Asynchronous API calls using the `Fetch API` for a smooth user experience.
* **Google Fonts:** Utilizing 'Poppins' for a professional look.

---

## 📦 Project Structure

```text
/pykv-project
  ├── main.py            # FastAPI Backend Logic & Auth
  ├── index.html         # Landing Page
  ├── register.html      # User Registration Page
  ├── login.html         # Secure Login Page
  ├── dashboard.html     # Main Storage Control Panel
  ├── js/
  │    └── app.js        # Frontend Logic & API Integration
  └── css/
       └── style.css     # Global Styles & Layouts


⚙️ How to Run
Install Dependencies:

Bash
pip install fastapi uvicorn python-jose[cryptography] python-multipart
Start the Backend:

Bash
uvicorn main:app --reload
Open the Frontend: Simply open index.html in your favorite web browser (or use Live Server in VS Code).

## 🔄 How the Data Flow Works

| Action | Frontend Method | API Endpoint | Backend Logic | Authorization |
| :--- | :--- | :--- | :--- | :--- |
| **SET** | `fetch(BASE + "/set")` | `POST /set` | Receives JSON and saves the key-value pair into the `store` dictionary. | **Required** (JWT) |
| **GET** | `fetch(BASE + "/get/{key}")` | `GET /get/{key}` | Searches the `store` dictionary for the key and returns the value. | **Required** (JWT) |
| **LIST** | `fetch(BASE + "/list")` | `GET /list` | Returns the entire `store` dictionary to populate the dashboard table. | **Required** (JWT) |
| **DELETE**| `fetch(BASE + "/delete/{key}")`| `DELETE /delete/{key}` | Removes the specific key from the dictionary using the `.pop()` or `del` method. | **Required** (JWT) 

### 🧠 Logic Explanation

1. **The Request:** When you click a button (e.g., "Store Data"), the JavaScript gathers your input and sends it as a "Request" to the FastAPI server.
2. **The Security Check:** The server looks at the `Authorization` header. If the JWT token is missing or wrong, it sends back a `401 Unauthorized` error.
3. **The Execution:** If authorized, Python modifies the `store = {}` dictionary in `main.py`.
4. **The Response:** The server sends back a `200 OK` status, and the Frontend JavaScript triggers `refreshTable()` to show you the new data immediately.
