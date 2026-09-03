# Intro to MIS: Interactive PaaS Demo
# Copyright: Suresh L. Paul

from flask import Flask, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Global Tech Hubs - Live Status</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 40px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto; }
        h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .status { font-weight: bold; color: #27ae60; }
        .metric { font-size: 1.2em; margin: 15px 0; }
        .footer { margin-top: 20px; font-size: 0.85em; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌐 Live MIS Cloud Dashboard</h2>
        <p class="status">● Server Status: Online (PythonAnywhere PaaS)</p>
        <div class="metric">📍 Active Region: <b>{{ region }}</b></div>
        <div class="metric">⚡ Server Load: <b>{{ load }}%</b></div>
        <div class="metric">👥 Active Demo Users: <b>{{ users }}</b></div>
        <p><i>Refresh the page to see real-time dynamic data updates!</i></p>
        <div class="footer">Course: Intro to MIS | Copyright: Suresh L. Paul</div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    regions = ["New York", "London", "Tokyo", "Singapore", "Frankfurt"]
    return render_template_string(
        HTML_TEMPLATE,
        region=random.choice(regions),
        load=random.randint(12, 45),
        users=random.randint(100, 500)
    )

if __name__ == "__main__":
    app.run()
