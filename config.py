import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.rbi.org.in"
START_URL = "https://www.rbi.org.in/Scripts/NotificationUser.aspx"
DOWNLOAD_DIR = "notification_data"
TEXT_DIR = os.path.join(DOWNLOAD_DIR, "extracted_text")
SUMMARY_DIR = os.path.join(DOWNLOAD_DIR, "text_summary")
SEEN_FILE = "seen_notifications.json"
METADATA_FILE = "processed_notifications.json"

## Email Configurations
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

## LLM Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)



