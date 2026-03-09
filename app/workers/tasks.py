import time 
import uuid 
from sqlalchemy import select 

from app.workers.celery_app import celery_app
from app.db.session_sync import SessionLocal
from app.db.models import Job
from app.services.pdf_parser import extract_text_from_pdf
from app.services.groq_client import analyze_resume_with_groq


@celery_app.task
def process_resume(job_id: str):

    '''
    
    1. Mark STARTED
    2. Do dummy work / pdf parsing 
    3. Mark SUCCESS / groq analysis
    '''
    job_uuid = uuid.UUID(job_id)

    db=SessionLocal()
    try:
        job = db.execute(select(Job).where(Job.id == job_uuid)).scalar_one_or_none()
        if not job:
            return {"error": "job not found"}
        
        #start hoga worker or status ko STARTED kr dega
        job.status = "STARTED"
        db.commit()

        #Abhi ke liye ek dummy task
        #time.sleep(2)

        #our real task
        if not job.stored_path:
            job.status = "FAILED"
            db.commit()
            return {"error": "Path is missing"}
        
        text = extract_text_from_pdf(job.stored_path)

        #Here we are getting response from groq and adding it to db 
        analysis = analyze_resume_with_groq(text)
        score = analysis.get("overall_score")
        if not isinstance(score, int):
            job.status="FAILED"
            db.commit()
            return{"error":"Groq response missing valid overall_score"}

        job.analysis_json = analysis 
        job.score = score
        job.extracted_text = text
        job.status = "SUCCESS"
        db.commit()

        return {"job_id":job_id, "status":"SUCCESS"}
    
    except Exception as e:
        if "job" in locals() and job:
            job.status = "FAILED"
            db.commit()
            return {"error": str(e)}
    finally:
        db.close()


 
