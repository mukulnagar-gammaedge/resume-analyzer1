import json 
from groq import Groq 

from app.core.config import settings

def analyze_resume_with_groq(resume_text: str) -> dict:
    
    client = Groq(api_key=settings.groq_api_key)

    prompt =  f"""
               You are a resume analyzer.
Return ONLY valid JSON with these keys:
- strengths: list of strings
- weaknesses: list of strings
- missing_skills: list of strings
- overall_score: integer from 0 to 100
- summary: string
Resume text:
{resume_text}
""".strip()
    
    resp = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": "You return only JSON. No extra text."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    content = resp.choices[0].message.content
    data = json.loads(content)
    return data 