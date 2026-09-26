import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = Path(__file__).resolve()
MODEL = os.getenv('MODEL', 'qwen/qwen3.8-27b:free')

