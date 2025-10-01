import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/ytscout")
REGION_CODES = [c.strip() for c in os.getenv("REGION_CODES", "US,GB,AU,IN,CA,DE,BR,JP").split(",") if c.strip()]
