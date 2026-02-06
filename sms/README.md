
# 📘 SMS Full-Stack Project – Resume Notes (SAVE THIS FILE)

## 👤 Owner

**Mohammed Sohail**

---

## 🧱 Project Overview

**School Management System (SMS)** – Full-stack, production-style project.

### Tech Stack

* **Backend**: Django, Django REST Framework, JWT (SimpleJWT)
* **Async**: Celery + Redis
* **Frontend**: React (Vite)
* **Reverse Proxy**: Nginx
* **Containers**: Docker & Docker Compose
* **Domains**:

  * Backend/Admin: `master.sohaildevops.site`
  * Frontend (planned): `student.sohaildevops.site`

---

## ✅ Current Status (VERY IMPORTANT)

### 🔙 Backend – STABLE ✅

* Django running behind Nginx
* Admin:

  ```
  http://master.sohaildevops.site/admin/
  ```
* Health:

  ```
  http://master.sohaildevops.site/health/ → {"status":"ok"}
  ```
* Auth APIs WORKING:

  * `POST /api/v1/auth/login/`
  * `GET /api/v1/auth/me/`
* JWT authentication verified

### `/me/` API Response Format

```json
{
  "success": true,
  "data": {
    "email": "sohailkhan88008@gmail.com",
    "first_name": "md",
    "last_name": "sohail",
    "roles": []
  }
}
```

---

### 🎨 Frontend – WORKING (95%) ✅

* React + Vite running on:

  ```
  http://13.201.41.29:5173
  ```
* Login works
* JWT stored in `localStorage`
* Dashboard renders:

  ```
  🎓 Student Dashboard
  Loading profile...
  Logout
  ```

👉 This means:

* Auth flow = DONE
* Token handling = DONE
* Dashboard routing = DONE
* Only **profile render mapping** remains

---

## 🧠 Key Concepts Learned (DO NOT FORGET)

### 1️⃣ Token vs Profile

* **Token controls login/dashboard**
* **Profile is just data**
* Dashboard visibility should depend on token, not profile

### 2️⃣ API Contract Awareness

* Login API returns:

  ```json
  { "access": "...", "refresh": "..." }
  ```
* Profile API returns:

  ```json
  { "success": true, "data": {...} }
  ```
* Frontend MUST read:

  ```js
  result.data
  ```

### 3️⃣ Dev CORS Best Practice

* Use **Vite proxy** (`/api → backend`)
* Do NOT directly call backend domain from frontend in dev
* Avoid CORS headaches

---

## 📄 Frontend File Reference

**File**: `sms_frontend/src/App.jsx`

Important states:

* `isLoggedIn` → controls dashboard
* `access_token` → stored in `localStorage`
* `fetchProfile()` → calls `/api/v1/auth/me/`

Current screen proves:

```
🎓 Student Dashboard
Loading profile...
```

Frontend logic is CORRECT.

---

## 🔧 EXACT NEXT STEP (WHEN RESUMING)

### 🎯 Goal

Show real user data instead of **“Loading profile…”**

### Fix to Apply

Open:

```bash
nano sms_frontend/src/App.jsx
```

In `fetchProfile()` ensure **THIS EXACT LOGIC**:

```js
const result = await response.json();
setProfile(result.data);
```

(Not `setProfile(result)` and NOT `setProfile(data)`)

Then:

```bash
npm run dev -- --host
```

Refresh browser.

### Expected Result

```
🎓 Student Dashboard
Email: sohailkhan88008@gmail.com
Name: md sohail
Role: Student
```

---

## 🛣️ Roadmap (After This)

### Frontend

* Fetch student data:

  * `/api/v1/academics/students/`
* Add routing (React Router)
* Improve UI (CSS / Tailwind)

### DevOps / Production

* Dockerize frontend
* Serve React build via Nginx
* Map domain:

  ```
  student.sohaildevops.site
  ```
* Enable HTTPS (Let’s Encrypt)
* Optional: Kubernetes later

---

## 🧠 Mentor Final Summary

You have:

* Built a real backend
* Built a real frontend
* Implemented JWT auth
* Solved Docker, CORS, React state issues
* Reached **dashboard stage**

You are **NOT stuck**.
You are **one small render fix away from completion**.

---

## ▶️ Resume Command

When you come back, say:

> **“Mentor, resume from dashboard profile rendering”**

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

ubuntu@ip-172-31-1-67:~/sms_redesign/sms_frontend$ cat vite.config.js

```bash
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": {
        target: "http://master.sohaildevops.site",
        changeOrigin: true,
        secure: false,
      },
    },
  },
});

```
ubuntu@ip-172-31-1-67:~/sms_redesign/sms_frontend$ cat src/App.jsx

```bash
import { useState, useEffect } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [profile, setProfile] = useState(null);

  // Check token on page load
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setIsLoggedIn(true);
      fetchProfile(token);
    }
  }, []);

  const fetchProfile = async (token) => {
    try {
      const response = await fetch("/api/v1/auth/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const result = await response.json();
        // Backend returns { success: true, data: {...} }
        setProfile(result.data);
      }
    } catch (err) {
      console.error("Profile fetch failed", err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("Logging in...");

    try {
      const response = await fetch("/api/v1/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Login API returns { access, refresh }
        localStorage.setItem("access_token", data.access);
        setIsLoggedIn(true);
        setMessage("✅ Login successful!");
        fetchProfile(data.access);
      } else {
        setMessage("❌ Invalid credentials");
      }
    } catch (error) {
      console.error(error);
      setMessage("❌ Server error");
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setIsLoggedIn(false);
    setProfile(null);
  };

  // ================= DASHBOARD =================
  if (isLoggedIn) {
    return (
      <div style={{ padding: "40px", fontFamily: "Arial" }}>
        <h1>🎓 Student Dashboard</h1>

        {profile ? (
          <>
            <p><strong>Email:</strong> {profile.email}</p>
            <p>
              <strong>Name:</strong> {profile.first_name || "N/A"} {profile.last_name || ""}
            </p>
            <p><strong>Role:</strong> {profile.role || "Student"}</p>
          </>
        ) : (
          <p>Loading profile...</p>
        )}

        <button onClick={logout} style={{ marginTop: "20px" }}>
          Logout
        </button>
      </div>
    );
  }

  // ================= LOGIN =================
  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>School Management System</h1>
      <p>Student Portal</p>

      <form onSubmit={handleLogin} style={{ maxWidth: "300px" }}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />

        <button type="submit" style={{ width: "100%", padding: "8px" }}>
          Login
        </button>
      </form>

      <p style={{ marginTop: "15px" }}>{message}</p>
    </div>
  );
}

export default App;
```

ubuntu@ip-172-31-1-67:~/sms_redesign/sms_frontend$
