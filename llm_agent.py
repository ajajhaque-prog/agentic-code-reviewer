
import os
import time
import json
import re
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from utils import get_logger

load_dotenv(override=True)
logger = get_logger("LLMAgent")

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") # Default to what we found works or standard
API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

# Strict JSON Schema Prompt
REVIEW_PROMPT_TEMPLATE = """You are a senior {language} code reviewer.
Analyze the following code.

OUTPUT FORMAT:
Return a SINGLE valid JSON object. Do not add markdown backticks or extra text.
The JSON must strictly follow this schema:

{{
  "summary_markdown": "## Summary\\n\\n(A concise summary of the code and issues found)...",
  "findings": [
    {{
      "id": "F001",
      "title": "Short title",
      "description": "Detailed description",
      "severity": "high", 
      "line": 10,
      "recommendation": "Fix recommendation",
      "category": "security"
    }}
  ],
  "rating": {{
    "quality": 7.5,
    "security": 6.0,
    "maintainability": 8.0,
    "overall": 7.2
  }}
}}

RULES:
1. "severity" must be: critical, high, medium, low, or info.
2. "category" examples: security, robustness, style, performance.
3. If code is empty or trivial, return a valid JSON with empty findings.

Context:
File: {filename}
Language: {language}

Code:
```{language}
{source_code}
```
"""

def clean_json_response(text: str) -> str:
    """Remove markdown backticks if present."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def generate_llm_review(source_code: str, filename: str, language: str) -> Dict[str, Any]:
    """
    Generate review using Gemini.
    Handles 429 Retry logic.
    """
    if not GEMINI_API_KEY:
        return _fallback_result(filename, language, "Missing API Key")

    prompt = REVIEW_PROMPT_TEMPLATE.format(
        language=language,
        filename=filename,
        source_code=source_code[:30000] # Safe chars limit
    )

    url = API_URL_TEMPLATE.format(model=GEMINI_MODEL, key=GEMINI_API_KEY)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4000}
    }

    retries = 3
    base_wait = 20 # Wait longer for free tier

    for attempt in range(retries):
        try:
            logger.info(f"Calling Gemini ({GEMINI_MODEL}) - Attempt {attempt+1}/{retries}")
            resp = requests.post(url, json=payload, timeout=60) # High timeout for large files
            
            if resp.status_code == 200:
                data = resp.json()
                try:
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    clean_text = clean_json_response(raw_text)
                    return json.loads(clean_text)
                except (KeyError, IndexError, json.JSONDecodeError) as e:
                    logger.error(f"Failed to parse success response: {e}")
                    # If parsing fails, retry might not help, but let's try strict repair if needed
                    # For now, return fallback with raw text
                    return _fallback_result(filename, language, f"Parse Error: {e}")

            elif resp.status_code == 429:
                logger.warning(f"Rate Limited (429). Waiting {base_wait}s...")
                time.sleep(base_wait * (attempt + 1)) # Linear backoff 20, 40, 60
                continue
            
            elif resp.status_code == 404:
                return _fallback_result(filename, language, f"Model {GEMINI_MODEL} not found (404). Check .env")

            else:
                logger.error(f"API Error {resp.status_code}: {resp.text}")
                return _fallback_result(filename, language, f"API Error {resp.status_code}")

        except Exception as e:
            logger.error(f"Network Exception: {e}")
            time.sleep(5)
    
    return _fallback_result(filename, language, "Rate Limit Exceeded (Fallback)")

def _fallback_result(filename: str, language: str, reason: str) -> Dict[str, Any]:
    """Mock result when API fails."""
    return {
        "summary_markdown": f"## Summary\n\n**Fallback Review** for `{filename}`.\n\nReason: {reason}",
        "findings": [
            {
                "id": "ERR01",
                "title": "Review Generation Failed",
                "description": f"Could not generate AI review: {reason}",
                "severity": "critical",
                "line": 0,
                "recommendation": "Check API Key, Quota, or Internet Connection.",
                "category": "infrastructure"
            }
        ],
        "rating": {
            "quality": 0.0,
            "security": 0.0,
            "maintainability": 0.0,
            "overall": 0.0
        }
    }
