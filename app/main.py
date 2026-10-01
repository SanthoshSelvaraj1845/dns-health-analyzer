from fastapi import FastAPI

from app.routes import router


app = FastAPI(
    title="DNS Health Analyzer",
    description="API for analyzing DNS health of a domain",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "DNS Health Analyzer API is running"
    }