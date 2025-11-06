# 🚀 IBM Full Stack Developer Capstone Project

This repository contains the final project developed as part of the **IBM Full Stack Software Developer Professional Certificate**.  
The goal of the project was to design, develop, and deploy a **cloud-based Full Stack application** integrating frontend, backend, and microservices.

---

## 🧩 Project Description

The application is a **Car Dealership Platform** that allows users to:
- List dealerships and view their details.
- Register and authenticate users (login, logout, register).
- Post and view reviews for each dealership.
- Analyze the sentiment of reviews using an AI-based microservice.

The system is composed of several integrated modules working under a distributed architecture deployed in the cloud.

---

## 🏗️ General Architecture

Frontend (React)  
↓  
Backend API (Django + REST)  
↓  
Sentiment Analysis Microservice (Flask + VADER)  
↓  
SQLite Database (persistence)  
↓  
Deployment on IBM Cloud Code Engine (Docker + Gunicorn)

---

## ⚙️ Technologies Used

| Layer | Technologies |
|-------|---------------|
| **Frontend** | React.js, HTML5, CSS3, Bootstrap |
| **Backend** | Django, Django REST Framework |
| **Microservice** | Flask, VADER Sentiment |
| **Database** | SQLite3 |
| **DevOps / Cloud** | Docker, IBM Cloud Code Engine |
| **Version Control** | GitHub Actions, Git |
| **Others** | Gunicorn, Python 3.10, Node.js |

---

## 🌐 Cloud Deployment

The project was **containerized and deployed on IBM Cloud Code Engine**, using a CI/CD pipeline powered by GitHub Actions and Docker.  

- 🌍 **Deployment URL:**  
  [https://django-dealership-app.229h9aaer3mu.us-south.codeengine.appdomain.cloud](https://django-dealership-app.229h9aaer3mu.us-south.codeengine.appdomain.cloud)

---

## 📸 Screenshots

| View | Description |
|------|--------------|
| `Home` | Main page with navigation. |
| `Dealer Details` | Dealership details with reviews. |
| `Post Review` | Form to submit a new review. |

---

## 💡 Key Learnings

During the development of this project, practical skills were gained in:
- Complete integration of a modern **Full Stack architecture**.
- Configuration and deployment in **serverless environments using Code Engine**.
- Error handling and debugging of **Docker containers in the cloud**.
- Communication between services (REST API + Flask microservice).
- Implementation of authentication and user management in Django.

---

## 👨‍💻 Author

**Rodrigo Opalo**  
📧 [https://www.linkedin.com/in/rodrigo-opalo/]  
🎓 Professional Certificate: *IBM Full Stack Software Developer (Coursera)*  
📅 Year: 2025

---

## 🪪 License

This project is licensed under the [Apache 2.0 License](./LICENSE).
