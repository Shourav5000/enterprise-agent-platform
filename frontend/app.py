import os
import streamlit as st
import requests

st.set_page_config(
    page_title="Enterprise Autonomous Incident Engine",
    page_icon="🤖",
    layout="wide"
)

# Dynamic backend URL configuration for production and local environments
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("🤖 Enterprise Autonomous Incident & Remediation Engine")
st.markdown("Multi-agent orchestration platform powered by LangGraph, FastAPI, and Anthropic Claude.")

# Sidebar for submitting incidents
st.sidebar.header("Submit New Incident")
incident_id_input = st.sidebar.text_input("Incident ID", value="INC-1002")
ticket_text_input = st.sidebar.text_area(
    "Ticket Description", 
    value="Database connection timeout and sql pool exhausted error occurring under heavy load during peak hours."
)

if st.sidebar.button("Run Agent Workflow"):
    if not ticket_text_input:
        st.sidebar.error("Please provide a ticket description.")
    else:
        payload = {
            "incident_id": incident_id_input,
            "raw_ticket_text": ticket_text_input
        }
        
        with st.spinner("Executing multi-agent workflow (Triage ➔ Remediation ➔ QA ➔ HITL)..."):
            try:
                response = requests.post(f"{BACKEND_URL}/api/incidents/triage", json=payload)
                if response.status_code == 200:
                    data = response.json()["result"]
                    st.session_state["last_result"] = data
                    st.success("Workflow executed successfully!")
                else:
                    st.error(f"API Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to FastAPI backend at {BACKEND_URL}.")

# Main display area for results
if "last_result" in st.session_state:
    res = st.session_state["last_result"]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Category", res.get("category", "N/A"))
    col2.metric("Urgency Score", f"{res.get('urgency_score', 0)} / 5")
    col3.metric("QA Status", res.get("qa_status", "PENDING"))
    
    st.subheader("🛠️ Generated Code Patch")
    st.code(res.get("generated_patch", "No patch generated."), language="python")
    
    st.subheader("📚 Retrieved RAG Vector Logs")
    for log in res.get("retrieved_logs", []):
        st.info(log)
        
    st.subheader("📋 Agent Execution Trace")
    for log_entry in res.get("execution_logs", []):
        st.text(log_entry)
        
    st.subheader("⚖️ Human-in-the-Loop Operator Gate")
    if res.get("requires_human_approval", True):
        st.warning("This patch requires explicit operator sign-off before production deployment.")
        c1, c2 = st.columns(2)
        if c1.button("✅ Approve & Deploy"):
            approval_res = requests.post(f"{BACKEND_URL}/api/incidents/approve?incident_id={res.get('incident_id')}&approved=true")
            st.success("Patch approved and deployed to production!")
        if c2.button("❌ Reject Patch"):
            st.error("Patch rejected by operator.")
    else:
        st.info("Auto-approved by policy.")
else:
    st.info("Submit an incident ticket from the sidebar to launch the agent pipeline.")