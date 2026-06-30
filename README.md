# CIMSTracker PWT Edition: Multi-Agent NCCHC Verification Pipeline

An enterprise-grade compliance simulation engine designed to automate forensic log auditing, isolate logging variances, and enforce human-governed remediation safety workflows within high-liability institutional environments.

## 📋 Problem Statement & Real-World Context
In correctional environments, administrative compliance directly correlates to inmate safety and facility risk mitigation. Missing a mandatory 30-minute high-risk suicide prevention check or mismanaging patient meal refusals creates catastrophic legal and systemic vulnerabilities. 

**CIMSTracker PWT Edition** provides a robust Proof of Concept (POC) demonstrating how decoupled autonomous agent systems can ingest operational telemetry data streams, catch intentional log tampering via deterministic filters, map operational exceptions to national regulatory standards, and preserve absolute data authority through Human-in-the-Loop (HITL) gatekeepers.

---

## 🧠 System Architecture & Multi-Agent Design

Instead of relying on a fragile, single "mega-prompt," this application utilizes a **split-labor cognitive graph** to separate analytical duties cleanly:

1. **Forensic Data Auditor Agent:** Isolates precise check-in timestamps, quantifies interval baseline deviations, and calculates protocol overage metrics.
2. **NCCHC Correlator Agent:** Maps operational exceptions directly onto national standards—specifically surface-flagging variances under **J-G-05** (Suicide Prevention Checks), **J-A-08** (Continuous Quality Improvement), and **J-E-01** (Nutrition & Patient Refusals).
3. **Deposition Strategist Agent:** Aggregates telemetry patterns to mathematically evaluate liability risk profiles and constructs clear, actionable remediation directives.

### 🛡️ Deterministic Tool Integration (Agent Skills)
To safeguard against LLM mathematical hallucinations, the ingestion pipeline routes incoming JSON payloads through a hardcoded **Python validation skill layer**. This script scans the data arrays first, isolating impossible log tampering exceptions—such as identical 0-minute and impossible -1-minute check records—before data ever touches the generative model.

### ⚠️ Human-in-the-Loop (HITL) Safety Gate
To prevent unauthorized automatic data publication or actions on live backend repositories, the system state machine forces a structural breakpoint. High-stakes forensic evaluations remain frozen in an immutable `PENDING_HUMAN_REVIEW` phase. The compliance supervisor must manually audit the dynamically compiled remediation draft and explicitly click **Authorize & Commit** to sign the block and append it to the sealed ledger.

---

## 🚀 Setup & Local Deployment Instructions

Follow these steps to run the interactive dashboard workspace locally:

### 1. Clone the Repository & Navigate
\`\`\`bash
git clone https://github.com/accessdenied7419/Multi-Agent-NCCHC-Verification-Pipeline.git
cd Multi-Agent-NCCHC-Verification-Pipeline
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install fastapi uvicorn pydantic
\`\`\`

### 3. Launch the Uvicorn Production Server
\`\`\`bash
python3 -m uvicorn submission_frontend.main:app --host 0.0.0.0 --port 8080
\`\`\`

### 4. Access the Interface
Open your browser and navigate to:
\`\`\`text
http://localhost:8080
\`\`\`

---

## ⚙️ Interactive Core Workspace Walkthrough
* **🎲 Randomize Queue Logs:** Mutates active session variables in memory to simulate changing institutional CAD ingestion feeds.
* **Execute NCCHC Audit:** Triggers the multi-agent graph evaluation and renders the compliance exception hold report.
* **Authorize & Commit:** Validates the state machine breakpoint, cryptographically seals the transaction block, and commits the records.
* **Reset Workspace:** Restores all session buffers cleanly back to the baseline operating parameters.
