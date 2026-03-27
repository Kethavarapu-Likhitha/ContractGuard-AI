from fastapi import FastAPI, UploadFile, File
import shutil
from services.pdf_service import extract_text

app = FastAPI()

@app.get("/")
def home():
    return {"message": "ContractGuard AI Backend Running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    # Save file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text(file_path)

    return {
        "filename": file.filename,
        "extracted_text": text[:1000]  # limit output
    }