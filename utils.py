import os
import logging
import uuid
import datetime
from typing import Dict, Any

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CodeReviewer")

def get_logger(name: str):
    return logging.getLogger(name)

def generate_report_id() -> str:
    """Generate a unique 8-char ID for reports."""
    return str(uuid.uuid4())[:8]

def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Language Map
EXT_LANG = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "react",
    ".tsx": "react",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".json": "json"
}

def detect_language(filename: str) -> str:
    """Detect language from file extension."""
    _, ext = os.path.splitext(filename.lower())
    return EXT_LANG.get(ext, "text")
