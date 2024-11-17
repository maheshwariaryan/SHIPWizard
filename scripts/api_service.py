# api_service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pandas as pd
from trainedbot import MLInsuranceQA  # Import from your existing model file

# Define request/response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    service_category: str | None = None
    confidence: float | None = None

# Initialize FastAPI app
app = FastAPI(
    title="Insurance QA API",
    description="API for insurance coverage questions and answers",
    version="1.0.0"
)

# Global variable for our QA system
qa_system = None

@app.on_event("startup")
async def startup_event():
    """Initialize the QA system on startup"""
    global qa_system
    
    data = pd.read_csv('domestic health.csv')
    
    try:
        qa_system = MLInsuranceQA(data, model_path="insurance_model")
        print("QA system initialized successfully!")
    except Exception as e:
        print(f"Error initializing QA system: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to initialize QA system")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Insurance QA API is running",
        "version": "1.0.0",
        "endpoints": {
            "/ask": "POST - Ask an insurance-related question",
            "/health": "GET - Check API health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if qa_system is None:
        raise HTTPException(status_code=503, detail="QA system not initialized")
    return {"status": "healthy", "qa_system": "initialized"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Endpoint to ask insurance-related questions"""
    if qa_system is None:
        raise HTTPException(status_code=503, detail="QA system not initialized")
    
    try:
        # Get answer from the QA system
        answer = qa_system.get_answer(request.question)
        
        # Extract service category if possible (this is optional and depends on your needs)
        service_category = None
        try:
            service_category = answer.split('\n')[0].split(':')[0].replace('For ', '')
        except:
            pass
        
        return AnswerResponse(
            answer=answer,
            service_category=service_category,
            confidence=None  # You could add confidence scores if you modify the model to return them
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api_service:app", host="0.0.0.0", port=8000, reload=True)