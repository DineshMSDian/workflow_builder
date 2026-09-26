import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = Path(__file__).resolve()
MODEL = 'google/gemini-2.5-flash-lite'

