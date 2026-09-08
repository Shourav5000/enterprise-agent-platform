from langgraph.graph import StateGraph, END
from .state import IncidentState
from .agents.triage import triage_incident_node
from .agents.remediation import remediation_node
from .agents.QA import qa_verification_node

def human_approval_node(state: IncidentState) -> IncidentState:
    """
    HITL Node: Evaluates whether the patch requires manual operator sign-off.
    """
    if state.requires_human_approval:
        state.execution_logs.append("[HITL] Execution paused. Patch requires explicit human approval before deployment.")
    else:
        state.execution_logs.append("[HITL] Auto-approval enabled. Proceeding to deployment.")
    return state

def create_incident_workflow():
    workflow = StateGraph(IncidentState)
    
    # Register nodes
    workflow.add_node("triage", triage_incident_node)
    workflow.add_node("remediation", remediation_node)
    workflow.add_node("qa", qa_verification_node)
    workflow.add_node("approval", human_approval_node)
    
    # Define edges
    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "remediation")
    workflow.add_edge("remediation", "qa")
    workflow.add_edge("qa", "approval")
    workflow.add_edge("approval", END)
    
    return workflow.compile()

compiled_workflow = create_incident_workflow()