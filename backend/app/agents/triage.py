from ..state import IncidentState

def triage_incident_node(state: IncidentState) -> IncidentState:
    """
    Triage Agent: Parses raw ticket text, determines category, 
    and assigns an initial urgency score based on keyword heuristics or LLM processing.
    """
    text = state.raw_ticket_text.lower()
    
    # Categorization logic
    if "database" in text or "sql" in text or "timeout" in text:
        state.category = "Database & Performance"
        state.urgency_score = 4
    elif "auth" in text or "login" in text or "token" in text:
        state.category = "Security & Authentication"
        state.urgency_score = 5
    else:
        state.category = "General System Error"
        state.urgency_score = 2
        
    state.execution_logs.append(f"[TriageAgent] Categorized incident as '{state.category}' with urgency {state.urgency_score}.")
    return state