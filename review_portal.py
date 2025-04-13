from flask import Flask, request, render_template_string, redirect
import json
from pathlib import Path

app = Flask(__name__)
INCIDENTS_PATH = Path("logs/incidents.json")

@app.route("/review")
def review():
    incident_id = int(request.args.get("incident_id"))

    with open(INCIDENTS_PATH) as f:
        incidents = json.load(f)

    if incident_id >= len(incidents):
        return "Incident not found.", 404

    incident = incidents[incident_id]

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TrustLayer Compliance Review</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f5f5f5;
                font-family: 'Helvetica Neue', Arial, sans-serif;
                padding: 30px;
                color: #212121;
            }}
            .review-card {{
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                padding: 40px;
                max-width: 800px;
                margin: 0 auto;
                border-left: 4px solid #000;
            }}
            .header {{
                margin-bottom: 30px;
                border-bottom: 1px solid #eee;
                padding-bottom: 20px;
            }}
            .incident-id {{
                background-color: #000;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
                font-size: 14px;
                display: inline-block;
                margin-bottom: 15px;
                letter-spacing: 0.5px;
            }}
            .risk-indicator {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: 600;
                color: white;
                background-color: {{'#000' if incident['confidence'] > 0.7 else '#555' if incident['confidence'] > 0.5 else '#888'}};
                margin-left: 10px;
                letter-spacing: 1px;
                vertical-align: middle;
            }}
            .message-area {{
                background-color: #f8f8f8;
                border-left: 3px solid #000;
                padding: 18px;
                margin: 20px 0;
                border-radius: 4px;
                font-family: monospace;
            }}
            .section {{
                margin-bottom: 24px;
            }}
            .label {{
                font-weight: 600;
                color: #000;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 13px;
            }}
            .actions {{
                margin-top: 35px;
                display: flex;
                gap: 15px;
                justify-content: flex-end;
            }}
            .confirm-btn {{
                background-color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 4px;
                color: white;
                font-weight: 500;
                transition: all 0.2s;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 14px;
            }}
            .confirm-btn:hover {{
                background-color: #333;
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .ignore-btn {{
                background-color: white;
                border: 1px solid #000;
                padding: 12px 24px;
                border-radius: 4px;
                color: #000;
                font-weight: 500;
                transition: all 0.2s;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 14px;
            }}
            .ignore-btn:hover {{
                background-color: #f5f5f5;
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            }}
            .progress {{
                background-color: #eee;
                border-radius: 0;
                height: 8px !important;
                margin-top: 8px;
            }}
            .progress-bar {{
                background-color: #000;
                color: transparent;
                height: 8px;
            }}
            .confidence-value {{
                font-weight: bold;
                margin-top: 8px;
            }}
            h2 {{
                font-weight: 300;
                letter-spacing: 0.5px;
            }}
            .badge {{
                background-color: #000 !important;
                color: white !important;
                font-weight: 500;
                padding: 6px 10px;
                border-radius: 4px;
                letter-spacing: 1px;
            }}
        </style>
    </head>
    <body>
        <div class="review-card">
            <div class="header">
                <div class="incident-id">INCIDENT #{incident_id}</div>
                <h2>Compliance Review
                <span class="risk-indicator">
                    {{'HIGH RISK' if incident['confidence'] > 0.7 else 'MEDIUM RISK' if incident['confidence'] > 0.5 else 'LOW RISK'}}
                </span>
                </h2>
            </div>
            
            <div class="section">
                <div class="label">User</div>
                <div><strong>{incident['user']}</strong></div>
            </div>
            
            <div class="section">
                <div class="label">Message</div>
                <div class="message-area">{incident['message']}</div>
            </div>
            
            <div class="section">
                <div class="label">Policy Violation</div>
                <div><strong>{incident['article']}</strong> – {incident['matched_policy']}</div>
            </div>
            
            <div class="section">
                <div class="label">AI Confidence Score</div>
                <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: {incident['confidence']*100}%;" 
                         aria-valuenow="{incident['confidence']*100}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <div class="confidence-value">{incident['confidence']:.2f}</div>
            </div>
            
            <div class="section">
                <div class="label">Violation Summary</div>
                <div>{incident['violation_summary']}</div>
            </div>
            
            <div class="section">
                <div class="label">AI Analysis</div>
                <div>{incident['risk_reason']}</div>
            </div>
            
            <div class="section">
                <div class="label">System Action</div>
                <div><span class="badge">{incident['action_taken'].upper()}</span></div>
            </div>
            
            <form method="post" action="/confirm">
                <input type="hidden" name="incident_id" value="{incident_id}">
                <div class="actions">
                    <button type="submit" name="decision" value="ignore" class="ignore-btn">
                        Dismiss Incident
                    </button>
                    <button type="submit" name="decision" value="confirm" class="confirm-btn">
                        Confirm Violation
                    </button>
                </div>
            </form>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/confirm", methods=["POST"])
def confirm():
    incident_id = int(request.form["incident_id"])
    decision = request.form["decision"]

    with open(INCIDENTS_PATH) as f:
        incidents = json.load(f)

    incidents[incident_id]["manager_confirmed"] = decision == "confirm"

    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=2)

    return f"✅ Decision saved. Incident {incident_id} marked as: {decision.upper()}."

if __name__ == "__main__":
    app.run(port=5000, debug=True)
