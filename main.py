from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import SymptomInput, TriageResult
from app.agent import run_triage_agent

app = FastAPI(
    title="AI Medical Triage Agent",
    description="An agentic AI that triages patient symptoms using tool-calling",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "Medical Triage Agent is running", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/triage", response_model=TriageResult)
def triage_patient(patient_input: SymptomInput):
    try:
        result = run_triage_agent(patient_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))