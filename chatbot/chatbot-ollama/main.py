from fastapi import FastAPI, UploadFile, File
import os
import shutil
from utils.pdf_parser import extract_text_from_pdf
from utils.vector_store import create_vector_store
from utils.ollama_chain import create_qa_chain

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vector_db = None
qa_chain = None

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(file_path)

        global vector_db, qa_chain
        vector_db = create_vector_store([text])
        qa_chain = create_qa_chain(vector_db)

        return {"filename": file.filename, "detail": "File uploaded and processed successfully."}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
async def ask_question(question: str):
    if not qa_chain:
        return {"answer": "Upload a PDF first."}
    
    result = qa_chain.run(question)
    return {"answer": result}
