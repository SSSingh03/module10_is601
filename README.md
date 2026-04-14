# Module 10 - FastAPI Docker Application

## 📌 Project Overview
This project is a Dockerized FastAPI application that integrates with a PostgreSQL database. It demonstrates building a backend API, containerizing it with Docker, and implementing CI/CD using GitHub Actions. The application allows users to be created and stored securely with hashed passwords.

---

## 🚀 Features
- FastAPI backend API
- PostgreSQL database integration
- SQLAlchemy ORM for database operations
- Password hashing for security
- Docker & Docker Compose setup
- Automated testing with Pytest
- CI/CD pipeline using GitHub Actions
- Docker Hub image deployment

---

## 🛠️ Technologies Used
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose
- Pytest
- GitHub Actions

---

## 📂 Project Structure

module10_is601/
│
├── app/
│ ├── auth/
│ ├── models/
│ ├── operations/
│ ├── schemas/
│ ├── config.py
│ ├── database.py
│ └── database_init.py
│
├── tests/
│ ├── integration/
│ └── unit/
│
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md


---

## ⚙️ How to Run the Application

### 1. Clone the Repository
```bash
git clone https://github.com/SSSingh03/module10_is601.git
cd module10_is601
2. Run with Docker
docker compose up --build
3. Access the API
FastAPI Docs:
http://localhost:8000/docs
🧪 Running Tests
Activate Virtual Environment (if using locally)
python3 -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Run Tests
pytest -v
🔁 CI/CD Pipeline

This project uses GitHub Actions to:

Run automated tests
Build Docker images
Push images to Docker Hub
🐳 Docker Hub Repository
https://hub.docker.com/r/ssingh1119/module10_is601
