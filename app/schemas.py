from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    domain: str = Field(..., min_length=3)


class AnalysisResponse(BaseModel):
    analysis_id: str
    domain: str
    status: str


class AnalysisResultResponse(BaseModel):
    analysis_id: str
    domain: str
    status: str
    result: dict