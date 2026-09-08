import os
from anthropic import Anthropic
from ..state import IncidentState
from ..tools.vector_store import vector_store

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def remediation_node(state: IncidentState) -> IncidentState:
    """
    Remediation Agent: Uses Anthropic Claude and vector store logs 
    to draft a targeted code fix for the incident.
    """
    state.execution_logs.append("[RemediationAgent] Querying vector store for similar incident context...")
    matched_logs = vector_store.search_similar_logs(state.raw_ticket_text)
    state.retrieved_logs = matched_logs
    
    prompt = f"""
    You are an expert DevOps and Site Reliability Engineer. 
    Incident Category: {state.category}
    Urgency Score: {state.urgency_score}/5
    Ticket: "{state.raw_ticket_text}"
    
    Historical Context/Similar Fixes:
    {matched_logs}

    Write a precise, production-grade code patch or configuration fix snippet to resolve this incident. Keep it concise and clean.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        state.generated_patch = response.content[0].text
        state.execution_logs.append("[RemediationAgent] Generated AI-powered patch successfully using Claude.")
    except Exception as e:
        state.generated_patch = f"# Fallback Patch\n# Error: {str(e)}\n# Solution: {matched_logs[0]}"
        state.execution_logs.append("[RemediationAgent] Claude API call failed. Used RAG fallback patch.")
        
    return state