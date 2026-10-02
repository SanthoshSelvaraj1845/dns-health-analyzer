from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router as analysis_router
from app.database import client


# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="DNS Health Analyzer",
    description=(
        "A FastAPI application for analyzing DNS records "
        "and DNSSEC health of a domain."
    ),
    version="1.0.0"
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================================================
# HTML TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# API ROUTES
# =========================================================

app.include_router(analysis_router)


# =========================================================
# FRONTEND HOME PAGE
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get(
    "/health",
    tags=["Health"]
)
def health_check():

    try:

        # Test MongoDB connection
        client.admin.command("ping")

        return {
            "status": "healthy",
            "service": "DNS Health Analyzer",
            "database": "connected",
            "version": "1.0.0"
        }

    except Exception as error:

        return {
            "status": "unhealthy",
            "service": "DNS Health Analyzer",
            "database": "disconnected",
            "error": str(error)
        }