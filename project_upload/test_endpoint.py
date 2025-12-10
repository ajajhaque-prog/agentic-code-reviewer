import requests
import os
import json

def test_endpoint():
    # URL of the API
    url = "http://127.0.0.1:8001/api/review"
    
    # File to upload
    file_path = "testandReview.py"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print(f"Sending {file_path} to {url}...")
    
    try:
        with open(file_path, "rb") as f:
            files = {"files": (file_path, f, "text/x-python")}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            print("\nSUCCESS!")
            data = response.json()
            print(f"Report ID: {data.get('report_id')}")
            print(f"PDF Path: {data.get('pdf_report')}")
            
            # Check for errors in the LLM response
            if data.get("structured", {}).get("findings", []) and "fallback" in data.get("llm_summary", "").lower():
                 print("\nWARNING: Fallback mode detected!")
            
            print("\nFULL RESPONSE:")
            print(json.dumps(data, indent=2))
        else:
            print(f"\nFAILED: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure the server is running: uvicorn app:app --reload")

if __name__ == "__main__":
    test_endpoint()
