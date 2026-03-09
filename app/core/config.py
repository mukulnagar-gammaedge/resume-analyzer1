from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    app_name: str = "Resume Analyzer API"
    env: str = "dev"

    database_url: str
    sync_database_url: str

    celery_broker_url: str
    celery_result_backend: str

    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    class Config:
        env_file=".env"

settings = Settings()
