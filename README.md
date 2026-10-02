# DNS Health Analyzer

A **FastAPI-based DNS Health Analyzer** that analyzes a domain's DNS records, performs basic DNSSEC configuration detection, evaluates domain health, and stores analysis results in **MongoDB Atlas**.

The project includes a responsive frontend dashboard and is deployed on **Render**.

## Features

- DNS record analysis: A, AAAA, MX, NS, TXT
- Basic DNSSEC detection using DNSKEY and DS records
- Domain health status
- Unique `analysis_id` for every analysis
- MongoDB Atlas integration
- FastAPI REST API
- Pydantic input validation
- Swagger API documentation
- Responsive HTML/CSS/JavaScript frontend
- Pytest testing
- Docker support
- Render deployment

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, Uvicorn
- **DNS:** dnspython
- **Database:** MongoDB Atlas, PyMongo
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Testing:** Pytest
- **Deployment:** Docker, Render
- **Version Control:** Git, GitHub

## API Endpoints

### Health Check


GET /api/v1/health


### Start DNS Analysis


POST /api/v1/analysis


Request:


{
  "domain": "google.com"
}


Response:


{
  "analysis_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "domain": "google.com",
  "status": "completed"
}


### Get Analysis Result


GET /api/v1/analysis/{analysis_id}


Returns the stored DNS records, health status, and DNSSEC information.

## Project Structure


dns-health-analyzer/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── database.py
│   ├── config.py
│   └── dns_analyzer.py
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


## Environment Variables

Create a `.env` file:


MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=dns_health_db


> Do not commit `.env` or database credentials to GitHub.

## Run Locally

Install dependencies:


pip install -r requirements.txt


Start the application:


uvicorn app.main:app --reload


Open:


http://127.0.0.1:8000


Swagger documentation:


http://127.0.0.1:8000/docs


## Docker


docker compose up --build


## Testing


pytest


## Live Deployment

**Live Application:**  
https://dns-health-analyzer.onrender.com

**Swagger API:**  
https://dns-health-analyzer.onrender.com/docs

**Health Check:**  
https://dns-health-analyzer.onrender.com/api/v1/health

## Application Flow


User enters domain
        ↓
FastAPI API
        ↓
DNS / DNSSEC Analysis
        ↓
MongoDB Atlas
        ↓
Analysis ID
        ↓
Retrieve Result
        ↓
Frontend Dashboard


## DNSSEC Note

The current implementation performs basic DNSSEC configuration detection using **DNSKEY and DS records**. It does not perform full cryptographic DNSSEC chain-of-trust validation.

## Status

**Successfully developed, tested, containerized, and deployed on Render.**

