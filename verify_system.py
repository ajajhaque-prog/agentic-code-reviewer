
import requests
import os
import json
import time

API_URL = "http://127.0.0.1:8002/api/review"
DOWNLOAD_URL = "http://127.0.0.1:8002/api/download-latest"
TEST_FILE = "testandReview.py"

def verify_system():
    if not os.path.exists(TEST_FILE):
        print(f"Error: {TEST_FILE} not found.")
        return

    print(f"Testing API: {API_URL}")
    print(f"Uploading: {TEST_FILE}")

    try:
        # 1. Upload File
        start_time = time.time()
        with open(TEST_FILE, "rb") as f:
            files = {"file": (TEST_FILE, f, "text/x-python")}
            response = requests.post(API_URL, files=files, timeout=70) # > 60s server timeout
        
        duration = time.time() - start_time
        print(f"Response Time: {duration:.2f}s")

        if response.status_code != 200:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
            return

        data = response.json()
        print("\nSUCCESS! API Response Received.")
        
        # 2. Validate Response Structure
        print("Validating JSON Structure...")
        structured = data.get("structured", {})
        if not structured:
            print("WARNING: 'structured' field is empty!")
            print(json.dumps(data, indent=2))
        else:
            required_keys = ["summary_markdown", "findings", "rating"]
            missing = [k for k in required_keys if k not in structured]
            if missing:
                print(f"FAILED: Missing keys in structured output: {missing}")
            else:
                print("External JSON Structure: OK")
                print(f"Findings: {len(structured.get('findings', []))}")
                print(f"Rating: {structured.get('rating')}")
                
        # 3. Verify PDF
        pdf_path = data.get("pdf_report")
        print(f"\nPDF Report Path listed: {pdf_path}")
        if pdf_path and os.path.exists(pdf_path):
             print(f"PDF File Exists on Server: YES ({os.path.getsize(pdf_path)} bytes)")
        else:
             print("PDF File Exists on Server: NO (Check temp dir)")

        # 4. Test Download
        print("\nTesting Download Endpoint...")
        dl_resp = requests.get(DOWNLOAD_URL)
        if dl_resp.status_code == 200:
            print(f"Download Success! Content Length: {len(dl_resp.content)} bytes")
        else:
            print(f"Download Failed: {dl_resp.status_code}")

    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    verify_system()
