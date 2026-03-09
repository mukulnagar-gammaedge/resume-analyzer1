

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
