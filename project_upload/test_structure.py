import os
import json
from llm_agent import generate_llm_review

# Mock data
source_code = """
def add(a, b):
    return a + b

def divide(a, b):
    return a / b
"""

summary = {
    "filename": "test_math.py",
    "language": "python",
    "issues": []
}

print("Running LLM Agent Test...")
try:
    result = generate_llm_review(source_code, summary)
    print(f"Method: {result.get('method')}")
    
    structured = result.get("structured")
    if not structured:
        print("ERROR: No structured data returned.")
        exit(1)
        
    print("\nStructured Data Keys:", structured.keys())
    
    # Validation against USER REQUEST requirement
    required_root_keys = {"summary_markdown", "findings", "rating"}
    if not required_root_keys.issubset(structured.keys()):
        print(f"FAILURE: Missing root keys. Found: {structured.keys()}")
        exit(1)

    findings = structured.get("findings", [])
    print(f"Findings Count: {len(findings)}")
    
    if findings:
        f = findings[0]
        required_finding_keys = {"id", "title", "description", "severity", "line", "recommendation", "category"}
        if not required_finding_keys.issubset(f.keys()):
             print(f"FAILURE: Finding missing keys. Found: {f.keys()}")
             exit(1)
        print("First Finding Keys Verified.")
        
    rating = structured.get("rating")
    print("Rating:", rating)
    required_rating_keys = {"quality", "security", "maintainability", "overall"}
    if not required_rating_keys.issubset(rating.keys()):
        print(f"FAILURE: Rating missing keys. Found: {rating.keys()}")
        exit(1)
    
    print("\nSUCCESS: Structure STRICTLY matches requirements.")
        
except Exception as e:
    print(f"\nEXCEPTION: {e}")
    exit(1)
