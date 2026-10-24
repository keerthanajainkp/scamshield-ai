"""
ScamShield AI - Flask Web Application
=====================================
This is the main Python backend application.
It uses Flask, a lightweight Python web framework, to:
1. Serve the frontend webpage (HTML, CSS, JavaScript).
2. Provide an API endpoint (/api/analyze) that takes a message, runs rule checks,
   and returns the findings and risk score as JSON.
"""

import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from flask import Flask, render_template, request, jsonify, send_file
from detector import analyze_message

app = Flask(__name__)

# Basic route: When you open http://127.0.0.1:5000 in your browser,
# Flask renders and displays the HTML page from the templates folder.
@app.route("/")
def home():
    return render_template("index.html")


# Slides route: Present directly in any browser with arrow keys
@app.route("/slides")
def slides():
    return render_template("slides.html")


# Download route: Instantly downloads the PowerPoint presentation in the browser
@app.route("/download-ppt")
def download_ppt():
    ppt_path = "ScamShield_AI_Presentation.pptx"
    return send_file(ppt_path, as_attachment=True, download_name="ScamShield_AI_Presentation.pptx")


# API route: When the user clicks "Analyze Message" on the frontend,
# JavaScript sends the message text here to be evaluated by our detector.
@app.route("/api/analyze", methods=["POST"])
def analyze_endpoint():
    try:
        data = request.get_json(silent=True) or {}
        message_text = data.get("message", "")
        
        # Call the rule-based detection engine in detector.py
        result = analyze_message(message_text)
        return jsonify(result), 200
    except Exception as error:
        # Return a safe, beginner-friendly error response if something unexpected occurs
        return jsonify({
            "error": "Failed to analyze message",
            "details": str(error),
            "risk_level": "Low",
            "risk_score": 0,
            "findings": []
        }), 500


# Simple health check endpoint to verify server is running
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "service": "ScamShield AI"}), 200


if __name__ == "__main__":
    print("=" * 60)
    print("ScamShield AI Server is starting!")
    print("Open your web browser and navigate to: http://127.0.0.1:5000")
    print("Press CTRL+C in this terminal when you want to stop the server.")
    print("=" * 60)
    # debug=True automatically reloads the app if you edit code
    app.run(host="127.0.0.1", port=5000, debug=True)
