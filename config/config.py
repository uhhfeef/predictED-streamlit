import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_URI = os.getenv("DB_URI", "sqlite:///database/edtech.db")
