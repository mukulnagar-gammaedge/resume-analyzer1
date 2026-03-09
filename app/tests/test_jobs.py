

#sync
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_job_status(fake_job_id):
    response = client.get(f"/jobs/{fake_job_id}")
    assert response.status_code in [200, 404, 422]
    if response.status_code == 200:
        data = response.json()
        assert data["job_id"] == fake_job_id
        assert data["status"] in ["PENDING", "SUCCESS", "FAILED"]
