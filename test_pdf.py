import os
import tempfile
from pdf_report import build_pdf_report_multi

# Mock data matching the new structure
files_map = {
    "test_file.py": {
        "source": "def foo():\n    pass",
        "language": "python",
        "structured": {
            "summary_markdown": "## Summary\n\nThis is a test summary.",
            "findings": [
                {
                    "id": "F001",
                    "title": "Test Finding",
                    "description": "This is a test finding description.",
                    "severity": "medium",
                    "line": 10,
                    "recommendation": "Fix it.",
                    "category": "testing"
                }
            ],
            "rating": {
                "quality": 8.0,
                "security": 9.0,
                "maintainability": 7.0,
                "overall": 8.0
            }
        }
    }
}

metadata = {
    "report_id": "TEST-001",
    "date": "2025-12-04",
    "time": "12:00:00"
}

output_path = "test_report.pdf"

print("Generating PDF report...")
try:
    build_pdf_report_multi(files_map, output_path, metadata)
    if os.path.exists(output_path):
        print(f"SUCCESS: PDF generated at {output_path}")
    else:
        print("FAILURE: PDF file not found.")
except Exception as e:
    print(f"EXCEPTION: {e}")
