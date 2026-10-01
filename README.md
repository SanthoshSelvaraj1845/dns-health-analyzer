# DNS Health Analyzer

A **FastAPI-based DNS Health Analyzer** that analyzes a domain's DNS records and DNSSEC configuration, evaluates its health status, and stores the analysis results in **MongoDB Atlas**.

The application is containerized using **Docker** and deployed on **Render** as a public REST API.

## Features

* DNS health analysis
* DNS record analysis (A, AAAA, MX, etc.)
* DNSSEC analysis
* Unique `analysis_id` generation
* MongoDB Atlas integration
* REST API using FastAPI
* Swagger API documentation
* Input validation using Pydantic
* Automated testing using pytest
* Docker & Docker Compose support
* Render cloud deployment

## Architecture


Client / Swagger
       |
       v
    FastAPI
       |
       v
 DNS Analyzer
       |
       +-------> DNS / DNSSEC
       |
       v
 MongoDB Atlas




##  Technologies

* Python
* FastAPI
* Pydantic
* MongoDB Atlas
* PyMongo
* DNS / DNSSEC
* Uvicorn
* Pytest
* Docker
* Docker Compose
* Git & GitHub
* Render


## API Endpoints

### Health Check


GET /api/v1/health


Response:


{
  "status": "healthy"
}


### Start Analysis


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




## Database

**MongoDB Atlas**


Database: dns_health_db
Collection: analyses


Analysis requests and results are stored in MongoDB.



## Run with Docker

Build and start the application:


docker compose up --build


Local API:


http://localhost:8000


Swagger:


http://localhost:8000/docs




## Testing

Run the test suite:


pytest




## Live Deployment

**Live API:**

https://dns-health-analyzer.onrender.com

**Swagger Documentation:**

https://dns-health-analyzer.onrender.com/docs

**Health Check:**

https://dns-health-analyzer.onrender.com/api/v1/health



## Project Structure


dns-health-analyzer/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── database.py
│   └── dns_analyzer.py
│
├── tests/
│   ├── test_analysis.py
│   ├── test_database.py
│   └── test_health.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md




## Environment Variables

Create a `.env` file:


MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=dns_health_db


> `.env` and database credentials must not be committed to GitHub.


## Project Status

* DNS Analysis
* DNSSEC Analysis
* FastAPI REST API
* MongoDB Atlas
* Pytest
* Docker
* GitHub
* Render Deployment

**Status: Successfully deployed and running.**
