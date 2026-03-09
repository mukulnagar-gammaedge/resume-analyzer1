#asyncly operate krne ke liye 
'''import pytest 
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_upload_resume_success(sample_pdf):
    # yaha pe humko fixture ne ek sample pdf bnna ke diya h
     transport = ASGITransport(app=app, lifespan="on")
     async with AsyncClient(transport=transport, base_url="http://test") as ac:
          with open(sample_pdf, "rb") as f:
               response = await ac.post("/resumes", files={"file": ("sample.pdf", f , "application/pdf")})
     assert response.status_code==200'''

#syncly operate krne ke liye 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_resume_success(sample_pdf):
    with open(sample_pdf, "rb") as f:
        response = client.post("/resumes", files={"file": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data

def test_upload_resume_missing_file():
    response = client.post("/resumes", files={})
    assert response.status_code == 422
