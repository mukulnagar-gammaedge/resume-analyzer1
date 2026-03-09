from fastapi import APIRouter, Depends, HTTPException , UploadFile, File
import uuid
import os
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession 

from app.workers.tasks import process_resume
from app.db.models import Job
from app.db.session import get_db 



router = APIRouter()

UPLOAD_DIR = "uploads"






@router.get("/health")
def health():
    return {"status":"ok"}

@router.post("/jobs")
async def create_job(db: AsyncSession = Depends(get_db)):
    job = Job(status="PENDING")
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return {"job_id": str(job.id), "status": job.status}


@router.get("/jobs/{job_id}")
async def get_job(job_id: uuid.UUID, db: AsyncSession=Depends(get_db)):
    stmt = select(Job).where(Job.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        print("job not found")
    
    return {"job_id": str(job.id), 
            "status": job.status,
            "original_filename": job.original_filename,
            "stored_path": job.stored_path,
            "content_type": job.content_type,
            "extracted_text": job.extracted_text,
            "score": job.score,
            "analysis_json": job.analysis_json,
            }


@router.post("/resumes")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail = "Only .pdf files are allowed")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    job = Job(status="PENDING", original_filename=file.filename, content_type=file.content_type)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    stored_filename = f"{job.id}.pdf"
    stored_path = os.path.join(UPLOAD_DIR, stored_filename)
    
    contents=await file.read()
    with open(stored_path, "wb") as f:
        f.write(contents)


    job.stored_path= stored_path
    await db.commit()

    process_resume.delay(str(job.id))

    return {"job_id": str(job.id), "status": job.status}



    






