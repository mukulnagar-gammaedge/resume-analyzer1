




import pytest


@pytest.fixture
def sample_pdf(tmp_path):
    #ye hume ek temperory pdf dega tesing ke liye
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n% Fake PDF content")
    return pdf_path

@pytest.fixture
def fake_job_id():
    #yaha humne ek fake id generate ki h 
    return "test-job-123"


