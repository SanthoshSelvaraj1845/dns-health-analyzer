from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_start_analysis():
    response = client.post(
        "/api/v1/analysis",
        json={
            "domain": "google.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis_id" in data