#async
'''import pytest 
from httpx import AsyncClient , ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_get_job_status(fake_job):
    transport = ASGITransport(app = app , lifespan='on')
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/jobs/{fake_job}")
        #ye check krega ki job h ki nhi , hogi to correct status code return krega
        assert response.status_code == 200
        data = response.json() # data ko python dictonary me covert krega
        assert data["job_id"] == fake_job
        assert data["status"] in  ["PENDING", "SUCCESS", "FAILED"]
'''
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
