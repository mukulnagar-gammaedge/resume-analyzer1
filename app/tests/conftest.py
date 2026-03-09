




import pytest
from unittest.mock import patch

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


'''@pytest.fixture(autouse=True)
def mock_celery_delay():
    
    with patch("app.api.routes.process_resume.delay") as mocked:
        mocked.return_value.id = "fake-job-id"
        yield mocked'''