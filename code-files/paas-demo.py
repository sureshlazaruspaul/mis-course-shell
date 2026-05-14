# For demo purposes
# Intro to MIS: PaaS
# Copyright: Suresh L. Paul

from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    current_time = datetime.now().strftime("%I:%M %p")
    return f"""
    <h1>Welcome to Intro to MIS</h1>
    <p>✅ Yes — this page is running right now.</p>
    <p>Current time: {current_time}</p>
    <p style="color:red;">This app is hosted on PythonAnywhere (PaaS).</p>
    """

if __name__ == "__main__":
    app.run()
