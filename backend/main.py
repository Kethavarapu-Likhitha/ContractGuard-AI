from fastapi import FastAPI, UploadFile, File
import shutil
from services.pdf_service import extract_text
from services.ai_service import analyze_contract
import json
app = FastAPI()

@app.get("/")
def home():
    return {"message": "ContractGuard AI Backend Running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    try:
        analysis = analyze_contract(text)

        print("AI RESPONSE:", analysis)

        try:
            analysis_json = json.loads(analysis)
        except Exception as e:
            print("JSON ERROR:", e)
            analysis_json = {"raw_output": analysis}

        return {
            "filename": file.filename,
            "analysis": analysis_json
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}