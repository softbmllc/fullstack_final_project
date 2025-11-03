import React, { useState } from "react";

export default function Register() {
  const [userName, setUserName]   = useState("");
  const [password, setPassword]   = useState("");
  const [email, setEmail]         = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName]   = useState("");
  const [busy, setBusy]           = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    try {
      const url = window.location.origin + "/djangoapp/register";
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, password, email, firstName, lastName }),
      });
      const json = await res.json();
      if (json.status) {
        sessionStorage.setItem("username", json.userName);
        window.location.href = window.location.origin;
      } else if (json.error === "Already Registered") {
        alert("The user with same username is already registered");
        window.location.href = window.location.origin;
      } else {
        alert("Register failed");
      }
    } catch {
      alert("Network error");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{
      maxWidth: 420,
      margin: "80px auto",
      padding: 24,
      background: "#fff",
      borderRadius: 10,
      boxShadow: "0 2px 10px rgba(0,0,0,.1)"
    }}>
      <h2 style={{textAlign:"center", color:"#333"}}>Sign Up</h2>
      <form onSubmit={submit}>
        {[
          ["Username", userName, setUserName],
          ["First Name", firstName, setFirstName],
          ["Last Name", lastName, setLastName],
          ["Email", email, setEmail],
          ["Password", password, setPassword, "password"]
        ].map(([label, val, fn, type="text"], i)=>(
          <div key={i} style={{marginBottom:16}}>
            <label style={{fontWeight:600}}>{label}</label><br/>
            <input
              type={type}
              value={val}
              onChange={e=>fn(e.target.value)}
              required={["Username","Password"].includes(label)}
              style={{
                width:"100%",
                padding:"8px 10px",
                border:"1px solid #ccc",
                borderRadius:6,
                marginTop:4
              }}
            />
          </div>
        ))}
        <button
          type="submit"
          disabled={busy}
          style={{
            width:"100%",
            background:"#4fbfc1",
            border:"none",
            color:"#fff",
            fontWeight:"bold",
            fontSize:"16px",
            padding:"10px",
            borderRadius:6,
            cursor:"pointer"
          }}>
          {busy ? "Registrando..." : "Register"}
        </button>
        <p style={{textAlign:"center", marginTop:16}}>
          <a href="/login/">Ir a Login</a>
        </p>
      </form>
    </div>
  );
}