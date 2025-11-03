import React from "react";
import Login from "./components/Login/Login";
import Register from "./components/Register/Register";
export default function App() {
  const path = window.location.pathname.replace(/\/+$/, "");
  if (path === "/login") return <Login />;
  if (path === "/register") return <Register />;
  return <div style={{padding:24}}>No React route for: {window.location.pathname}</div>;
}