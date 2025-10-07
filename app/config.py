from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

# Environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./yt_topics.db")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
