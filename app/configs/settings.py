import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    
settings = Settings()