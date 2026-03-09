
# ye wala code hum tab use krenge jab hum asyncly operate krna ho 
'''import pytest
from sqlalchemy import insert
from app.db import async_session
from app.db.models import Job

@pytest.fixture
def sample_pdf(tmp_path):
    # ye function humko ek temporary pdf dega testing ke liye 
    pdf_path = tmp_path
    pdf_path.write_bytes(b"%PDF-1.4\n% Fake PDF content ")
    return pdf_path


@pytest.fixture 
async def fake_job():
    # iss function se hum fake job banayenge 
    async with async_session() as session:
        stmt = insert(Job).values(
            id="test-job-123",
            status="PENDING",
            original_filename="sample.pdf",
            stored_path="/fake/path/sample.pdf",
            content_type="application/pdf",
            extracted_text="Fake resume text",
            score=0,
            analysis_json={"strengths": [], "overall_score": 0}
        )
        await session.execute(stmt)
        await session.commit()
    return "test-job-123"'''


 # ye code syncly operate krne ke liye 

'''
import pytest
from sqlalchemy import insert
from app.db import async_session
from app.db.models import Job

@pytest.fixture
def fake_job_id():
    return "test-job-123"

@pytest.fixture(autouse=True)
async def setup_fake_job(fake_job_id):
    async with async_session() as session:
        stmt = insert(Job).values(
            id=fake_job_id,
            status="PENDING",
            original_filename="sample.pdf",
            stored_path="/fake/path/sample.pdf",
            content_type="application/pdf",
            extracted_text="Fake resume text",
            score=0,
            analysis_json={"strengths": [], "overall_score": 0}
        )
        await session.execute(stmt)
        await session.commit()
'''
import pytest

@pytest.fixture
def sample_pdf(tmp_path):
    """Provide a temporary fake PDF file for testing uploads."""
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n% Fake PDF content")
    return pdf_path

@pytest.fixture
def fake_job_id():
    """Provide a fake job ID for testing job status endpoint."""
    return "test-job-123"

