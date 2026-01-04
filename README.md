# AI-Powered Hydration Tracking Assistant

An end-to-end **AI-powered hydration tracking system** that allows users to log daily water intake, receive intelligent hydration feedback using an LLM, and visualize their intake history through a clean dashboard.

This project demonstrates **AI + Backend + DevOps** skills by integrating LangChain, FastAPI, Streamlit, SQLite, and Docker.

---

## Features

- Log daily water intake per user  
- AI-generated hydration analysis using OpenAI (via LangChain)  
- Visualize intake history with charts  
- Persistent storage using SQLite  
- REST API built with FastAPI  
- Interactive dashboard built with Streamlit  
- Fully Dockerized (API + Dashboard)
- Secure handling of API keys using environment variables  

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
| Language | Python 3.12 |
| AI / LLM | OpenAI GPT-4o-mini |
| AI Framework | LangChain |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| Containerization | Docker & Docker Compose |
| Environment Mgmt | python-dotenv |

---

## Project Structure

```
AI-Powered-Hydration-Tracking-Assistant/
│
├── src/
│   ├── agent.py
│   ├── api.py
│   ├── database.py
│   ├── logger.py
│
├── dashboard.py
├── requirements.txt
├── Dockerfile.api
├── Dockerfile.dashboard
├── docker-compose.yml
├── .dockerignore
├── README.md
```

---

## Local Setup (Without Docker)

### 1️) Create Virtual Environment
```bash
python -m venv water_intake_tracker
water_intake_tracker\Scripts\activate
```

### 2️) Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️) Configure Environment Variables
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Run with Docker (Recommended)

```bash
docker compose up --build
```

- FastAPI Docs → http://localhost:8000/docs
- Streamlit Dashboard → http://localhost:8501

---

## 👤 Author

**Anuj Dhiraj Bhagat**  
B.Tech Computer Science
