from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .state import IncidentState
from .workflow import compiled_workflow

app = FastAPI(
    title="Autonomous Incident & Remediation Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "agent-remediation-engine"}

@app.post("/api/incidents/triage")
def trigger_incident_workflow(payload: IncidentState):
    result_state = compiled_workflow.invoke(payload)
    return {
        "message": "Incident workflow completed successfully.",
        "result": result_state
    }

@app.post("/api/incidents/approve")
def approve_incident_patch(incident_id: str, approved: bool):
    return {
        "incident_id": incident_id,
        "operator_approved": approved,
        "deployment_status": "DEPLOYED" if approved else "REJECTED_BY_OPERATOR"
    }