import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# LLM Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "moonshotai/kimi-k2-instruct")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "5000"))

# GitHub Configuration
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
DEFAULT_BRANCH = os.getenv("DEFAULT_BRANCH", "main")

# Agent Configuration
AGENT_VERBOSE = True
MAX_ITERATIONS = 10
requests_per_second = 0.5 # 1 request every 2s

# Accessibility Standards
WCAG_LEVELS = ["A", "AA", "AAA"]
ACCESSIBILITY_CATEGORIES = [
    "Perceivable",
    "Operable",
    "Understandable",
    "Robust"
]

# File Paths
REPORTS_DIR = "reports"
DATA_DIR = "data"
TEMP_DIR = "temp"

# Create directories if they don't exist
for directory in [REPORTS_DIR, DATA_DIR, TEMP_DIR]:
    os.makedirs(directory, exist_ok=True)
