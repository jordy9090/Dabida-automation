"""
DABIDA 자동화 시스템 설정 파일
"""
import os
from pathlib import Path
try:
    # Attempt to import load_dotenv for loading environment variables from
    # a .env file. If python‑dotenv is not installed, the import will fail
    # and we will skip loading from .env; environment variables must then
    # be set externally.
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None

# 프로젝트 루트: .../Dabida-automation === 
BASE_DIR = Path(__file__).resolve().parent.parent

# .env를 '명시적 경로'로 로드 (중요) ===
# Colab의 현재 작업 디렉토리와 무관하게 확실히 로드됨
ENV_PATH = BASE_DIR / ".env"
# Only call load_dotenv if it was successfully imported. This prevents
# ModuleNotFoundError when python‑dotenv is not available.
if load_dotenv is not None:
    load_dotenv(ENV_PATH)

# API Keys
OPENAI_API_KEY       = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY       = os.getenv('GEMINI_API_KEY')
YOUTUBE_CLIENT_ID    = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET= os.getenv('YOUTUBE_CLIENT_SECRET')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
NOTION_API_KEY       = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID   = os.getenv('NOTION_DATABASE_ID')

# 디버그 모드
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 로그 설정
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'automation.log'

# 파일 경로 설정
DATA_DIR = BASE_DIR / 'data'
VIDEO_OUTPUT_DIR = DATA_DIR / 'videos'
SCRIPT_OUTPUT_DIR = DATA_DIR / 'scripts'

# 영상 설정
VIDEO_SETTINGS = {
    'duration': 60,  # seconds
    'format': 'mp4',
    'resolution': (1080, 1920),  # 9:16 ratio for shorts
    'fps': 30
}

# API 설정
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# ChatGPT 설정
CHATGPT_MODEL = "gpt-4"
CHATGPT_MAX_TOKENS = 2000
CHATGPT_TEMPERATURE = 0.7

# Gemini 설정
GEMINI_MODEL = "gemini-pro"

print("✅ Settings loaded successfully!")
