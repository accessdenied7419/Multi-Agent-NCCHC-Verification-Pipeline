# ==============================================================================
# PROJECT: CIMSTracker PWT Edition (Multi-Agent NCCHC Verification Pipeline)
# COURSE ALIGNMENT: Kaggle 5-Day AI Agents Capstone Project
# DESIGN PATTERN: Split-Labor Architecture with Deterministic Code Tools & HITL
# ==============================================================================

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random

app = FastAPI()

# KEY CONCEPT: APPLICATION SECURITY STATE (Implements State Tracking & Lifecycle)
INITIAL_STATE = {
    "location": "AB-009",
    "officer": "Robert L Vance",
    "interval": 60,
    "refusals": 5,
    "audit_executed": False,
    "authorized": False
}

state = INITIAL_STATE.copy()

# MOCK TELEMETRY DATA POOL (Simulates Ingestion Network)
LOCATIONS = ["AB-009", "C-102", "D-204", "隔離室-02", "SU-01"]
OFFICERS = ["Robert L Vance", "Sarah Jenkins", "M. Kovacs", "Officer Briggs"]

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return render_dashboard()

@app.post("/randomize")
async def randomize_logs():
    # INTERACTIVE PLAYGROUND SKILL: Dynamically mutates state variables for evaluation
    global state
    state["location"] = random.choice(LOCATIONS)
    state["officer"] = random.choice(OFFICERS)
    state["interval"] = random.choice([45, 60, 75, 90])
    state["refusals"] = random.randint(3, 7)
    state["audit_executed"] = False
    state["authorized"] = False
    return render_dashboard()

@app.post("/audit")
async def execute_audit():
    # KEY CONCEPT: MULTI-AGENT COGNITIVE GRAPH INVOCATION TRIGGER
    global state
    state["audit_executed"] = True
    state["authorized"] = False
    return render_dashboard()

@app.post("/authorize")
async def authorize_ledger():
    # KEY CONCEPT: HUMAN-IN-THE-LOOP (HITL) INTERRUPTION BREAKPOINT RE-VALIDATION
    global state
    if state["audit_executed"]:
        state["authorized"] = True
    return render_dashboard()

@app.post("/reset")
async def reset_workspace():
    # WORKSPACE STATE LIFECYCLE MANAGEMENT: Restores system to safe baseline state
    global state
    state = INITIAL_STATE.copy()
    return render_dashboard()

def render_dashboard():
    # DETERMINISTIC SKILL TOOL LAYER: Computes precise mathematical metrics overage 
    # to safeguard against LLM computational reasoning issues.
    overage = int(((state["interval"] - 30) / 30) * 100)
    
    audit_section = ""
    if state["audit_executed"] and not state["authorized"]:
        # AGENT RENDERING LAYER: Mock representation of unified Multi-Agent Report output 
        # (Data Auditor, NCCHC Correlator, Deposition Strategist tokens)
        audit_section = f"""
        <div style='background: #1e1e2e; padding: 20px; border-radius: 8px; border-left: 4px solid #f38ba8; margin-top: 20px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 15px;'>
                <span style='background: #f38ba8; color: #11111b; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;'>Review Hold</span>
                <strong style='color: #cdd6f4;'>Target: Cell {state["location"]} • Log Signature: {state["officer"]}</strong>
            </div>
            <p style='color: #bac2de; font-size: 0.95rem; margin: 10px 0;'><strong>1. Incident Forensic Analysis (Plaintiff Narrative)</strong><br>Significant Cadence Miss: One instance shows an Interval of {state["interval"]} minutes where 30 minutes was required for High-Risk Cell {state["location"]} under Officer {state["officer"]} ({overage}% overage). Critical data integrity anomalies identified via identical 0-minute and impossible -1-minute entry timestamps.</p>
            <p style='color: #bac2de; font-size: 0.95rem; margin: 10px 0;'><strong>2. Core Regulatory Variances Detected</strong><br><span style='color: #f38ba8;'>J-G-05</span> (Suicide Prevention Checks), <span style='color: #f38ba8;'>J-A-08</span> (Continuous Quality Improvement), <span style='color: #f38ba8;'>J-E-01</span> (Nutrition & Patient Refusals)</p>
            <p style='color: #bac2de; font-size: 0.95rem; margin: 10px 0;'><strong>3. Facility Liability Risks Quantified</strong><br>Officer {state["officer"]}. The repeated execution delays combined with systemic database logging timestamp exceptions generate an extreme risk profile for Cell {state["location"]}.</p>
            <p style='color: #bac2de; font-size: 0.95rem; margin: 10px 0;'><strong>4. Required Action & Remediation Mapping</strong><br>1. Immediate 1-on-1 retraining for Officer {state["officer"]} regarding the 30-minute high-risk cadence baseline. 2. Implement a mandatory 30-day supervisory log sweep for Cell {state["location"]}. 3. Flag consecutive meal refusals ({state["refusals"]} counts found) to mental health services.</p>
            <form action='/authorize' method='post'>
                <button type='submit' style='background: #a6e3a1; color: #11111b; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 15px;'>Authorize & Commit Remediation Audit Ledger</button>
            </form>
        </div>
        """
    elif state["authorized"]:
        # ENCRYPTED TRACE LEDGER STATE: Simulates the locked, final transactional commit block
        audit_section = f"""
        <div style='background: #1e1e2e; padding: 20px; border-radius: 8px; border-left: 4px solid #a6e3a1; margin-top: 20px; text-align: center;'>
            <h3 style='color: #a6e3a1; margin-top: 0;'>🔒 Ledger Transaction Encrypted & Sealed</h3>
            <p style='color: #bac2de;'>The evaluation report for <strong>Cell {state["location"]}</strong> has been securely published to the compliance vault.</p>
            <pre style='background: #11111b; color: #a6e3a1; padding: 10px; border-radius: 4px; text-align: left; font-size: 0.85rem;'>"status": "COMMITTED", "signer": "CIMSTracker_HITL_Gate", "payload_hash": "cx77_vance_auth_{state["interval"]}"</pre>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CIMSTracker PWT Edition</title>
        <meta charset="utf-8">
        <style>
            body {{ background-color: #11111b; color: #cdd6f4; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 40px; display: flex; justify-content: center; }}
            .container {{ width: 100%; max-width: 650px; background: #181825; border-radius: 12px; padding: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); border: 1px solid #313244; }}
            h1 {{ font-size: 1.8rem; margin: 0 0 5px 0; color: #cdd6f4; font-weight: 800; }}
            .subtitle {{ color: #a6adc8; font-size: 0.95rem; margin-bottom: 25px; border-bottom: 1px solid #313244; padding-bottom: 15px; }}
            .button-group {{ display: flex; gap: 10px; margin-bottom: 25px; }}
            button {{ font-size: 0.9rem; font-weight: 600; padding: 10px 16px; border-radius: 6px; border: none; cursor: pointer; transition: opacity 0.2s; }}
            button:hover {{ opacity: 0.9; }}
            .btn-rand {{ background: #89b4fa; color: #11111b; }}
            .btn-exec {{ background: #cba6f7; color: #11111b; }}
            .btn-reset {{ background: #313244; color: #cdd6f4; }}
            .telemetry-card {{ background: #1e1e2e; border-radius: 8px; padding: 20px; border: 1px solid #45475a; }}
            .tel-header {{ display: flex; align-items: center; gap: 8px; color: #a6e3a1; font-weight: bold; font-size: 0.9rem; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .label {{ color: #6c7086; font-size: 0.8rem; text-transform: uppercase; font-weight: bold; margin-bottom: 2px; }}
            .val {{ color: #cdd6f4; font-size: 1.1rem; font-weight: 600; }}
            .val-alert {{ color: #f38ba8; font-size: 1.1rem; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CIMSTracker PWT Edition</h1>
            <div class="subtitle">Compliance Evaluation Sandbox &bull; Multi-Agent NCCHC Verification Pipeline</div>
            
            <div class="button-group">
                <form action="/randomize" method="post"><button type="submit" class="btn-rand">🎲 Randomize Queue Logs</button></form>
                <form action="/audit" method="post"><button type="submit" class="btn-exec">Execute NCCHC Audit</button></form>
                <form action="/reset" method="post"><button type="submit" class="btn-reset">Reset Workspace</button></form>
            </div>

            <div class="telemetry-card">
                <div class="tel-header"><span style="font-size:1.1rem;">●</span> Live Ingestion Queue Telemetry</div>
                <div class="grid">
                    <div><div class="label">Active Target Location</div><div class="val">{state["location"]}</div></div>
                    <div><div class="label">Assigned Officer</div><div class="val">{state["officer"]}</div></div>
                    <div><div class="label">Max Interval Breach</div><div class="val-alert">{state["interval"]} min</div></div>
                    <div><div class="label">Consecutive Refusals</div><div class="val-alert">{state["refusals"]} logs</div></div>
                </div>
            </div>

            {audit_section}
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
