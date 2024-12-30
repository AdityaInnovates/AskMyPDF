from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
import shutil
from db_connect import Base, engine, SessionLocal
from Models.models import  Document
from Models.models import  QuestionAnswer
from libs.allDirectories import allDirectories
from libs.process_pdf import process_pdf
from libs.get_qa_chain import get_qa_chain

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PDF Q&A API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API models
class QuestionRequest(BaseModel):
    document_id: int
    question: str

class QuestionResponse(BaseModel):
    answer: str
    document_id: int



for value in allDirectories.values():
    os.makedirs(value, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {
        "status": True,
        "serverTime": datetime.utcnow().isoformat()
    }

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        file_path = os.path.join(allDirectories["UPLOAD_DIR"], file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create database entry
        db = SessionLocal()
        db_document = Document(
            filename=file.filename,
            file_path=file_path
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Process PDF and create vector store
        vector_store_path = process_pdf(file_path, db_document.id)
        db_document.vector_store_path = vector_store_path
        db.commit()
        
        return {"document_id": db_document.id, "message": "File uploaded and processed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/question/", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about a specific document"""
    try:
        db = SessionLocal()
        document = db.query(Document).filter(Document.id == request.document_id).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Retrieve previous questions and answers for context
        previous_qa = db.query(QuestionAnswer).filter(QuestionAnswer.document_id == request.document_id).all()
        context = "\n".join([f"Q: {qa.question}\nA: {qa.answer}" for qa in previous_qa])
        qa_chain = get_qa_chain(document.vector_store_path)
        
        result = qa_chain({"query": f"{context}\nQ: {request.question}\nA:"})
        
        # Save question and answer in the database
        question_answer = QuestionAnswer(
            document_id=request.document_id,
            question=request.question,
            answer=result["result"]
        )
        db.add(question_answer)
        db.commit()
        
        return {
            "answer": result["result"],
            "document_id": request.document_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/documents/")
async def list_documents():
    """List all uploaded documents"""
    try:
        db = SessionLocal()
        documents = db.query(Document).all()
        return [{"id": doc.id, "filename": doc.filename, "upload_date": doc.upload_date} for doc in documents]
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
