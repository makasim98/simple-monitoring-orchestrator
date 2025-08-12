from flask import Flask, request, jsonify

app = Flask("Orchestrator")

monitored_endpoints = {}

@app.route('/')
def dashboard():
    return "<h1>Orchestrator Dashboard!!!</h1>" # return HTML

@app.route('/add')
def add_endpoint():
    return "<h1>ADDING</h1>" # return HTML

@app.route('/remove')
def remove_endpoint():
    return "<h1>REMOVING</h1>" # return HTML

app.run(host="0.0.0.0", port=5000, debug=True)