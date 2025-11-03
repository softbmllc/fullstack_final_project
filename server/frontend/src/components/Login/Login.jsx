import React, { useState } from "react";

export default function Login() {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    const url = window.location.origin + "/djangoapp/login";
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, password }),
    });
    const json = await res.json();
    if (json.status === "Authenticated") {
      sessionStorage.setItem("username", json.userName);
      window.location.href = window.location.origin;
    } else {
      alert("Login failed");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "40px auto" }}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <div style={{ marginBottom: 12 }}>
          <label>Username</label><br />
          <input value={userName} onChange={(e) => setUserName(e.target.value)} />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Password</label><br />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
      <p style={{ marginTop: 16 }}>
        <a href="/register">Register Now</a>
      </p>
    </div>
  );
}