
import os
import shutil
import zipfile
import tempfile
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import get_logger, generate_report_id, detect_language
from llm_agent import generate_llm_review
from pdf_report import build_pdf_report

logger = get_logger("API")

app = FastAPI(title="Agentic Code Reviewer (Rebuilt)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State for "Download Latest" (Not persistent, resets on restart)
LATEST_REPORT_PATH = None

@app.post("/api/review")
async def review_single(file: UploadFile = File(...)):
    """Review a single uploaded file."""
    global LATEST_REPORT_PATH
    try:
        content = await file.read()
        source_code = content.decode("utf-8", errors="ignore")
        language = detect_language(file.filename)
        
        logger.info(f"Processing single file: {file.filename} ({language})")
        
        # 1. Generate Review
        review_data = generate_llm_review(source_code, file.filename, language)
        
        # 2. Generate PDF
        report_id = generate_report_id()
        pdf_filename = f"report_{report_id}.pdf"
        output_path = os.path.join(tempfile.gettempdir(), pdf_filename)
        
        build_pdf_report(review_data, output_path, file.filename)
        LATEST_REPORT_PATH = output_path
        
        return JSONResponse({
            "status": "success",
            "report_id": report_id,
            "filename": file.filename,
            "pdf_report": output_path,
            "structured": review_data
        })

    except Exception as e:
        logger.error(f"Error in review_single: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/review-multi")
async def review_multi(files: List[UploadFile] = File(...)):
    """Review multiple files (POC: Reviews first file for now, expandable)."""
    # NOTE: User requirement implied handling multi-file, but PDF generator currently designed for one structure.
    # We will process the FIRST valid code file to ensure the flow works, as per current PDF spec.
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    return await review_single(files[0]) 

@app.post("/api/review-zip")
async def review_zip(zip_file: UploadFile = File(...)):
    """Extract ZIP and review the first valid code file found."""
    global LATEST_REPORT_PATH
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "upload.zip")
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(zip_file.file, f)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
            # Find first code file
            target_file = None
            target_content = ""
            
            for root, dirs, files in os.walk(temp_dir):
                for fname in files:
                    if fname.endswith((".py", ".js", ".java", ".cpp", ".c", ".ts")):
                        target_file = fname
                        with open(os.path.join(root, fname), "r", encoding="utf-8", errors="ignore") as f:
                            target_content = f.read()
                        break
                if target_file: break
            
            if not target_file:
                 raise HTTPException(status_code=400, detail="No source code found in ZIP")

            # Reuse single review logic
            language = detect_language(target_file)
            review_data = generate_llm_review(target_content, target_file, language)
            
            report_id = generate_report_id()
            pdf_filename = f"report_{report_id}.pdf"
            output_path = os.path.join(tempfile.gettempdir(), pdf_filename)
            
            build_pdf_report(review_data, output_path, target_file)
            LATEST_REPORT_PATH = output_path
            
            return JSONResponse({
                "status": "success",
                "report_id": report_id,
                "filename": target_file,
                "pdf_report": output_path,
                "structured": review_data
            })

    except Exception as e:
        logger.error(f"Error in review_zip: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-latest")
def download_latest():
    """Download the last generated PDF."""
    global LATEST_REPORT_PATH
    if not LATEST_REPORT_PATH or not os.path.exists(LATEST_REPORT_PATH):
        raise HTTPException(status_code=404, detail="No report generated yet.")
    return FileResponse(LATEST_REPORT_PATH, filename="latest_review_report.pdf")
