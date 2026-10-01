from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime, timezone

from app.database import analyses_collection
from app.dns_analyzer import analyze_domain
from app.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisResultResponse,
)


router = APIRouter(prefix="/api/v1", tags=["DNS Analysis"])


@router.post("/analysis", response_model=AnalysisResponse)
def start_analysis(request: AnalysisRequest):

    analysis_id = str(uuid4())

    document = {
        "analysis_id": analysis_id,
        "domain": request.domain,
        "status": "processing",
        "result": {},
        "created_at": datetime.now(timezone.utc),
    }

    analyses_collection.insert_one(document)

    try:
        result = analyze_domain(request.domain)

        analyses_collection.update_one(
            {"analysis_id": analysis_id},
            {
                "$set": {
                    "status": "completed",
                    "result": result,
                    "completed_at": datetime.now(timezone.utc),
                }
            },
        )

    except Exception as exc:

        analyses_collection.update_one(
            {"analysis_id": analysis_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(exc),
                }
            },
        )

        raise HTTPException(
            status_code=500,
            detail="DNS analysis failed",
        )

    return {
        "analysis_id": analysis_id,
        "domain": request.domain,
        "status": "completed",
    }


@router.get(
    "/analysis/{analysis_id}",
    response_model=AnalysisResultResponse,
)
def get_analysis(analysis_id: str):

    analysis = analyses_collection.find_one(
        {"analysis_id": analysis_id}
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    return {
        "analysis_id": analysis["analysis_id"],
        "domain": analysis["domain"],
        "status": analysis["status"],
        "result": analysis.get("result", {}),
    }