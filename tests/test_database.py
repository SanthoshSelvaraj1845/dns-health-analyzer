from app.database import client


def test_database_connection():
    result = client.admin.command("ping")

    assert result["ok"] == 1
    