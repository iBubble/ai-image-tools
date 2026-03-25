import os, json, time, random, urllib.request
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/pollinations/generate", methods=["POST"])
def pollinations_generate():
    body = request.json
    prompt = body.get("prompt", "")
    return jsonify({"status": "todo"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
