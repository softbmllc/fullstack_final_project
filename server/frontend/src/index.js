// server/frontend/src/index.js
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

try {
  const el = document.getElementById("root");
  createRoot(el).render(<App />);
} catch (e) {
  const pre = document.createElement("pre");
  pre.textContent = "BOOT ERROR:\n" + (e && e.stack || e);
  document.body.appendChild(pre);
}
window.onerror = (m,s,l,c,e)=> {
  const pre = document.createElement("pre");
  pre.textContent = "RUNTIME ERROR:\n" + (e && e.stack || m);
  document.body.appendChild(pre);
};