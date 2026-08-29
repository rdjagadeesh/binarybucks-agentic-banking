
# BinaryBucks Architecture 

This document provides the complete architectural view of the BinaryBucks agentic banking support system.  
It aligns with the system architecture including:  
Edge Layer, API, Security Controls, Coordinator Agent, Domain Agents, MCP Servers, Session Store, LLM Layer, Evaluation Suite, Observability, and future components.

---

## 1. Architecture Overview

BinaryBucks follows a layered, modular architecture:

- User Interface Layer  
- Edge & API Layer  
- Security & Control Layer  
- Coordinator & Agents Layer  
- Tools & MCP Servers Layer  
- LLM & Reasoning Layer  
- Session Store Layer  
- Observability Layer  
- Future Components (Evaluation Suite, Self-hosted LLM, Mortgages, etc.)

This structure mirrors enterprise agentic patterns while remaining fully simulated.

---

## 2. Full Architecture Diagram

```mermaid
flowchart TB

    %% UI Layer
    subgraph UI_LAYER["User Interface Layer"]
        UI["Chat UI and Dashboard"]
    end

    %% Edge Layer
    subgraph EDGE_LAYER["Edge and API Layer"]
        EDGE["Edge Layer (WAF, DDoS, Rate Limits, API Gateway)"]
        API["API Entry Point"]
    end

    %% Security Layer
    subgraph SECURITY_LAYER["Security and Control Layer"]
        AUTHN["Authentication (Identity Provider)"]
        AUTHZ["Authorization"]
        PII["PII Redaction"]
        EVAL["Agent Evaluation Suite (future)"]
        COST["Cost Tracker"]
    end

    %% Session Store
    subgraph SESSION_LAYER["Session Store"]
        SESSION["Conversation History and Inter-agent Shared State"]
    end

    %% LLM Layer
    subgraph LLM_LAYER["LLM and Reasoning Layer"]
        SELF_LLM["Self-hosted LLM (future)"]
        THIRD_LLM["Third-party LLM"]
        FAQ["RAG / FAQ Knowledge"]
    end

    %% Coordinator and Agents
    subgraph COORD_LAYER["Coordinator and Agents"]
        ORCH["Coordinator Agent"]
        ACC_AGENT["Accounts Agent"]
        TX_AGENT["Transactions Agent"]
        SVC_AGENT["Service Agent"]
        RISK_AGENT["Risk Agent"]
    end

    %% Tools and MCP Servers
    subgraph TOOLS_LAYER["Tools and MCP Servers"]
        ACC_MCP["Accounts MCP Server (Balance Enquiry)"]
        TX_MCP["Transactions MCP Server (Transaction Details, Statement Request)"]
        SVC_MCP["Service MCP Server (Address Change, Cheque Book, KYC Update, Mortgages)"]
    end

    %% Observability
    subgraph OBS_LAYER["Observability"]
        OBS["Observability (Prompts, Agent Calls, Tool Calls, CPU, Memory, Disk)"]
    end

    %% User Journey
    UI --> EDGE --> API

    %% Security Flow
    API --> AUTHN
    API --> PII
    API --> EVAL
    AUTHN --> AUTHZ
    API --> ORCH

    %% Coordinator & Session
    ORCH --> SESSION
    SESSION --> ORCH

    %% Coordinator to Agents
    ORCH --> ACC_AGENT
    ORCH --> TX_AGENT
    ORCH --> SVC_AGENT
    ORCH --> RISK_AGENT

    %% Agents to MCP Servers
    ACC_AGENT --> ACC_MCP
    TX_AGENT --> TX_MCP
    SVC_AGENT --> SVC_MCP
    RISK_AGENT --> TX_MCP
    RISK_AGENT --> SVC_MCP

    %% Agents to LLMs
    ORCH --> SELF_LLM
    ORCH --> THIRD_LLM
    ACC_AGENT --> THIRD_LLM
    TX_AGENT --> THIRD_LLM
    SVC_AGENT --> THIRD_LLM
    RISK_AGENT --> THIRD_LLM

    %% LLM to FAQ
    THIRD_LLM --> FAQ

    %% Policy & Guardrails
    ORCH --> AUTHZ
    ORCH --> EVAL

    %% Observability & Cost
    ORCH --> OBS
    ACC_AGENT --> OBS
    TX_AGENT --> OBS
    SVC_AGENT --> OBS
    RISK_AGENT --> OBS
    OBS --> COST

    %% Results back to user
    ORCH --> API --> EDGE --> UI
```

---

## 3. Component Summary

### User Interface Layer
- Chat UI  
- Dashboard  
- Quick actions  
- Memory display  

### Edge & API Layer
- WAF  
- DDoS protection  
- Rate limiting  
- API gateway  

### Security & Control Layer
- Authentication  
- Authorization  
- PII redaction  
- Agent evaluation suite (future)  
- Cost tracking  

### Coordinator & Agents Layer
- Coordinator agent  
- Accounts agent  
- Transactions agent  
- Service agent  
- Risk agent  

### Tools & MCP Servers Layer
- Accounts MCP  
- Transactions MCP  
- Service MCP  
- Future: mortgages, loans, onboarding  

### LLM & Reasoning Layer
- Third-party LLM  
- Self-hosted LLM (future)  
- FAQ / RAG knowledge  

### Session Store Layer
- Conversation history  
- Inter-agent shared state  

### Observability Layer
- Prompt logging  
- Agent call tracing  
- Tool call tracing  
- CPU/memory/disk metrics  
- Cost tracking  

---

## 4. Future Expansion

- Loans Agent  
- Mortgage Agent  
- Investment Agent  
- Identity/KYC Agent  
- Multi-turn workflows  
- Human review dashboards  
- Real RAG pipelines  
- Self-hosted LLM integration  

---

## 5. Disclaimer

BinaryBucks is a **simulated** system.  
It does **not** access real banking systems, real customer data, or perform real financial actions.  
All examples, profiles, and risk scores are fictional and for demonstration purposes only.


---
