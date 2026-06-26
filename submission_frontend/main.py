import os
import json
import random
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CIMSTracker PWT - NCCHC Compliance Engine")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SIMULATED_SESSION = {
    "status": "IDLE",
    "cell_id": "AB-001",
    "officer": "James M Dean",
    "draft_report": None,
    "current_cadence_minutes": 60,
    "consecutive_refusals": 3
}

@app.get("/api/randomize")
async def randomize_test_data():
    officers = ["James M Dean", "Sarah K Jenkins", "Robert L Vance", "Elena M Rostova"]
    cells = ["AB-001", "C-204", "SHU-04", "AB-009"]
    SIMULATED_SESSION["officer"] = random.choice(officers)
    SIMULATED_SESSION["cell_id"] = random.choice(cells)
    SIMULATED_SESSION["current_cadence_minutes"] = random.choice([45, 60, 75, 90, 120])
    SIMULATED_SESSION["consecutive_refusals"] = random.randint(3, 7)
    SIMULATED_SESSION["status"] = "IDLE"
    SIMULATED_SESSION["draft_report"] = None
    return SIMULATED_SESSION

@app.get("/api/simulate-trigger")
async def trigger_agent_pipeline():
    overage_pct = int(((SIMULATED_SESSION["current_cadence_minutes"] - 30) / 30) * 100)
    SIMULATED_SESSION["status"] = "PENDING_HUMAN_REVIEW"
    SIMULATED_SESSION["draft_report"] = {
        "smoking_gun": f"Significant Cadence Miss: One instance shows an Interval of {SIMULATED_SESSION['current_cadence_minutes']} minutes where 30 minutes was required for High-Risk Cell {SIMULATED_SESSION['cell_id']} under Officer {SIMULATED_SESSION['officer']} ({overage_pct}% overage). Critical data integrity anomalies identified via identical 0-minute and impossible -1-minute entry timestamps.",
        "standards_affected": ["J-G-05 (Suicide Prevention Checks)", "J-A-08 (Continuous Quality Improvement)", "J-E-01 (Nutrition & Patient Refusals)"],
        "weakest_link": f"Officer {SIMULATED_SESSION['officer']}. The repeated execution delays combined with systemic database logging timestamp exceptions generate an extreme risk profile for Cell {SIMULATED_SESSION['cell_id']}.",
        "remediation_plan": f"1. Immediate 1-on-1 retraining for Officer {SIMULATED_SESSION['officer']} regarding the 30-minute high-risk cadence baseline. 2. Implement a mandatory 30-day supervisory log sweep for Cell {SIMULATED_SESSION['cell_id']}. 3. Flag consecutive meal refusals ({SIMULATED_SESSION['consecutive_refusals']} counts found) to mental health services."
    }
    return {"message": "Success"}

@app.get("/api/pending")
async def get_pending():
    if SIMULATED_SESSION["status"] == "PENDING_HUMAN_REVIEW":
        return [SIMULATED_SESSION]
    return []

@app.post("/api/action")
async def approve_report():
    SIMULATED_SESSION["status"] = "COMPLETED_AND_ARCHIVED"
    return {"status": "SUCCESS", "message": "Forensic audit locked and archived to facility compliance ledger."}

@app.get("/api/reset")
async def reset_demo():
    SIMULATED_SESSION["status"] = "IDLE"
    SIMULATED_SESSION["draft_report"] = None
    return {"status": "RESET"}

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CIMSTracker PWT - NCCHC Compliance Engine</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-main: #0b0f19;
                --bg-card: #111827;
                --border-color: #1f2937;
                --text-primary: #f9fafb;
                --text-secondary: #9ca3af;
                --primary-blue: #2563eb;
                --primary-blue-hover: #1d4ed8;
                --accent-amber: #f59e0b;
                --status-red: #ef4444;
                --status-green: #10b981;
            }
            body { font-family: 'Inter', sans-serif; background-color: var(--bg-main); color: var(--text-primary); padding: 40px 20px; min-height: 100vh; margin: 0; }
            .container { max-width: 960px; margin: 0 auto; }
            
            /* Header */
            header { margin-bottom: 32px; }
            h1 { font-size: 28px; font-weight: 700; margin: 0 0 6px 0; color: var(--text-primary); letter-spacing: -0.02em; }
            .subtitle { color: var(--text-secondary); font-size: 14px; margin: 0; font-weight: 400; }
            
            /* Button Group Toolbar */
            .toolbar { display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }
            .btn { font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500; padding: 10px 18px; border-radius: 6px; cursor: pointer; transition: background-color 0.15s, border-color 0.15s; border: 1px solid transparent; }
            .btn-primary { background-color: var(--primary-blue); color: white; }
            .btn-primary:hover { background-color: var(--primary-blue-hover); }
            .btn-secondary { background-color: transparent; border-color: var(--border-color); color: var(--text-primary); }
            .btn-secondary:hover { background-color: #1f2937; border-color: #374151; }
            .btn-danger { background-color: transparent; border-color: transparent; color: var(--text-secondary); }
            .btn-danger:hover { color: var(--status-red); }
            
            /* Cards */
            .card { background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-top: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
            
            /* Telemetry Block Style */
            .telemetry-title { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-amber); margin: 0 0 20px 0; display: flex; align-items: center; gap: 8px; }
            .grid-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .metric-box { border-left: 2px solid var(--border-color); padding-left: 14px; }
            .metric-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }
            .metric-value { font-size: 16px; font-weight: 600; color: var(--text-primary); }
            .metric-alert { color: var(--status-red); }

            /* Review Center Block */
            .review-header { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 16px; margin-bottom: 20px; }
            .review-title-group { display: flex; align-items: center; gap: 12px; }
            .review-title { font-size: 18px; font-weight: 600; margin: 0; }
            .badge { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding: 4px 8px; border-radius: 4px; }
            .badge-warning { background-color: rgba(239, 68, 68, 0.15); color: var(--status-red); border: 1px solid rgba(239, 68, 68, 0.2); }
            .badge-success { background-color: rgba(16, 185, 129, 0.15); color: var(--status-green); border: 1px solid rgba(16, 185, 129, 0.2); }
            
            .report-section { margin-bottom: 18px; }
            .report-label { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.02em; }
            .report-text { font-size: 14px; line-height: 1.6; color: #d1d5db; margin: 0; }
            .text-highlight { color: #fca5a5; }
            
            pre { background-color: #0d1117; padding: 16px; border-radius: 6px; overflow-x: auto; font-family: 'Courier New', Courier, monospace; font-size: 13px; color: var(--status-green); border: 1px solid var(--border-color); }
            .status-msg { font-size: 14px; color: var(--text-secondary); margin-top: 16px; text-align: center; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>CIMSTracker PWT Edition</h1>
                <p class="subtitle">Compliance Evaluation Sandbox • Multi-Agent NCCHC Verification Pipeline</p>
            </header>
            
            <div class="toolbar">
                <button class="btn btn-secondary" onclick="randomizeData()">🎲 Randomize Queue Logs</button>
                <button class="btn btn-primary" onclick="triggerAgent()">Execute NCCHC Audit</button>
                <button class="btn btn-danger" onclick="resetDemo()">Reset Workspace</button>
            </div>
            
            <div id="telemetry-view" class="card">
                <div class="telemetry-title">● Live Ingestion Queue Telemetry</div>
                <div class="grid-metrics">
                    <div class="metric-box">
                        <div class="metric-label">Active Target Location</div>
                        <div id="tel-cell" class="metric-value">AB-001</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Assigned Officer</div>
                        <div id="tel-off" class="metric-value">James M Dean</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Max Interval Breach</div>
                        <div class="metric-value metric-alert"><span id="tel-int">60</span> min</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Consecutive Refusals</div>
                        <div class="metric-value metric-alert"><span id="tel-ref">3</span> logs</div>
                    </div>
                </div>
            </div>
            
            <div id="review-center">
                <p class="status-msg">Workspace synchronized. Ready to ingest telemetry cycles.</p>
            </div>
        </div>

        <script>
            async function randomizeData() {
                const res = await fetch('/api/randomize');
                const data = await res.json();
                document.getElementById('tel-cell').innerText = data.cell_id;
                document.getElementById('tel-off').innerText = data.officer;
                document.getElementById('tel-int').innerText = data.current_cadence_minutes;
                document.getElementById('tel-ref').innerText = data.consecutive_refusals;
                document.getElementById('review-center').innerHTML = '<p class="status-msg" style="color: var(--accent-amber);">Queue updated with randomized database slice. Core state reset to IDLE.</p>';
            }
            async function triggerAgent() {
                document.getElementById('review-center').innerHTML = '<p class="status-msg" style="color: var(--primary-blue);">Running cognitive graph compilation layers...</p>';
                await fetch('/api/simulate-trigger');
                await checkPending();
            }
            async function resetDemo() {
                await fetch('/api/reset');
                document.getElementById('tel-cell').innerText = "AB-001";
                document.getElementById('tel-off').innerText = "James M Dean";
                document.getElementById('tel-int').innerText = "60";
                document.getElementById('tel-ref').innerText = "3";
                document.getElementById('review-center').innerHTML = '<p class="status-msg">Workspace parameters cleared.</p>';
            }
            async function checkPending() {
                const res = await fetch('/api/pending');
                const data = await res.json();
                const container = document.getElementById('review-center');
                if(data.length === 0) {
                    container.innerHTML = '<p class="status-msg">No open audit reviews in queue.</p>';
                    return;
                }
                const session = data[0];
                container.innerHTML = `
                    <div class="card">
                        <div class="review-header">
                            <div class="review-title-group">
                                <h2 class="review-title">Manager Evaluation Center</h2>
                                <span class="badge badge-warning">Review Hold</span>
                            </div>
                            <div style="font-size: 13px; color: var(--text-secondary)">Target: <strong>Cell ${session.cell_id}</strong> • Log Signature: <strong>${session.officer}</strong></div>
                        </div>
                        
                        <div class="report-section">
                            <div class="report-label">1. Incident Forensic Analysis (Plaintiff Narrative)</div>
                            <p class="report-text">${session.draft_report.smoking_gun}</p>
                        </div>
                        <div class="report-section">
                            <div class="report-label">2. Core Regulatory Variances Detected</div>
                            <p class="report-text text-highlight">${session.draft_report.standards_affected.join(', ')}</p>
                        </div>
                        <div class="report-section">
                            <div class="report-label">3. Facility Liability Risks Quantified</div>
                            <p class="report-text">${session.draft_report.weakest_link}</p>
                        </div>
                        <div class="report-section">
                            <div class="report-label">4. Required Action & Remediation Mapping</div>
                            <p class="report-text" style="color: #a7f3d0;">${session.draft_report.remediation_plan}</p>
                        </div>
                        
                        <div style="margin-top:28px; padding-top: 20px; border-top: 1px solid var(--border-color); text-align: right;">
                            <button class="btn btn-primary" onclick="approveAction()">Authorize & Commit Remediation Audit Ledger</button>
                        </div>
                    </div>
                `;
            }
            async function approveAction() {
                const res = await fetch('/api/action', {method: 'POST'});
                const data = await res.json();
                document.getElementById('review-center').innerHTML = `
                    <div class="card" style="border-color: var(--status-green);">
                        <div class="review-header" style="border-bottom: none; margin-bottom: 0;">
                            <div class="review-title-group">
                                <h2 class="review-title" style="color: var(--status-green);">✓ Audit Action Executed & Finalized</h2>
                                <span class="badge badge-success">Committed</span>
                            </div>
                        </div>
                        <p style="font-size: 14px; color: var(--text-secondary); margin: 4px 0 20px 0;">Supervisor verification token applied. Audit metrics successfully transferred to immutable compliance database layers.</p>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    </div>
                `;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
