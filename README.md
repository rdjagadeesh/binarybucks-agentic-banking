
# BinaryBucks – Agentic Banking Support System 

BinaryBucks is a modular, multi‑agent support system designed to demonstrate how agentic architectures, safety guardrails, and tool‑augmented reasoning can be combined into a cohesive, production‑style codebase.  
All interactions, profiles, and risk assessments are fully simulated.

---

## 1. Overview

BinaryBucks provides:

- A modern chat‑based support interface  
- A multi‑agent backend (Account, Card, Risk)  
- Centralized LLM configuration  
- Centralized guardrails and policy enforcement  
- Tool‑augmented reasoning (profile lookup, risk scoring)  
- Conversation memory  
- Audit logging  
- Lightweight RAG using internal FAQ documents  
- A clean, extensible architecture suitable for scaling into more complex domains  

---

## 2. Agent Design

BinaryBucks uses a multi-agent pattern where each agent is autonomous, domain‑focused, and governed by shared safety rules.

### Design Principles
- Single responsibility per agent  
- Shared system prompt  
- Shared LLM configuration  
- Memory-aware responses  
- Tool-augmented reasoning  
- RAG-enhanced domain knowledge  
- Guardrail-enforced safety  

### Agent Flow
1. Orchestrator routes request  
2. Agent receives query, customer ID, memory, FAQ knowledge, and tool output  
3. Agent constructs structured prompt  
4. LLM generates response  
5. Orchestrator logs interaction  

---

## 3. Security Model

BinaryBucks implements a layered security model appropriate for simulated banking support.

### Guardrails
- No real financial actions  
- No transfers, refunds, or card blocks  
- No access to real accounts or systems  
- No legal or regulatory advice  
- High-risk cases require human review  
- All examples are fictional  

### Policy Enforcement
- Centralized keyword-based detection  
- Guardrails applied before agent routing  

### Prompt Safety
- Strict behavioral constraints  
- Agents cannot weaken guardrails  
- Controlled memory and RAG context  

### Observability
- Full audit logging  
- Traceable agent calls  
- Extendable for metrics and dashboards  

### Isolation
- No external API calls to real banking systems  
- All data simulated  
- Tools operate on mock data only  

---

## 4. Repository Structure

```
binarybucks-agentic-banking/
│
├── app.py
│
├── src/
│   ├── agents/
│   │   ├── account_agent.py       # extension specialist
│   │   ├── card_agent.py          # extension specialist
│   │   ├── risk_agent.py          # extension specialist
│   │   ├── transaction_agent.py   # extension specialist
│   │   ├── service_agent.py       # extension specialist
│   │   └── orchestrator.py        # active LLM boundary
│   │
│   ├── config/
│   │   ├── llm_config.py
│   │   └── policy.py
│   │
│   ├── prompts/
│   │   └── system_prompts.py
│   │
│   ├── tools/
│   │   ├── bank_tools.py
│   │   └── logging_tools.py
│   │
│   └── tools
│       
│
├── docs/
│   |── banking_faq.md
|   |── architecture.md
|   └── agent_design.md
│
├── tests/
│   └── test_support.py
└── binarybucks_audit.log          # generated locally; ignored by Git
```

---

## 5. Extensibility

BinaryBucks is structured to support future enhancements such as:

- Additional agents  
- External tool integrations  
- Real RAG pipelines  
- Authentication and identity layers  
- Observability dashboards  
- API gateway integration  
- Multi-turn intent classification  
- Human review dashboards  

### Production gaps

Before connecting real financial data, add authentication and authorization, a managed session store, PII redaction at the API boundary, structured/centralized audit logging, provider timeouts and retries, an evaluation suite, and real MCP/API integrations. The current customer profile, transactions, and risk scores are fixtures for demonstration only.

---

## 6. Disclaimer

BinaryBucks is a **simulated** system.  
It does **not** access real banking systems, real customer data, or perform real financial actions.  
All examples, profiles, and risk scores are fictional and for demonstration purposes only.

---
