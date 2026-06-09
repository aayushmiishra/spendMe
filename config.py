import os
import logging
from dotenv import load_dotenv

APP_NAME='spendME'
USER_ID='chiku'
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)