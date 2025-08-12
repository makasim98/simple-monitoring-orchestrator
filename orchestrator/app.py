from flask import Flask, jsonify

app = Flask("Orchestrator")

monitored_endpoints = {}

@app.route('/')
def dashboard():
    return "<h1>Orchestrator Dashboard!!!</h1>" # return HTML

# Get endpoint monitored by the Orchestrator
@app.route('/enpoints')
def add_endpoint():
    return "<h1>ADDING</h1>" # return HTML

# ADD New Endpoint to the monitored APIs
@app.route('/add_enpoint')
def add_endpoint():
    return "<h1>ADDING</h1>" # return HTML

# Remove existing Endpoint from the monitored APIs
@app.route('/remove_enpoint')
def remove_endpoint():
    return "<h1>REMOVING</h1>" # return HTML

# Deploy monitoring client to target remote server/vm
@app.route('/deploy')
def deploy_client():
    return "<h1>REMOVING</h1>" # return HTML

# Remove monitoring client from target remote server/vm
@app.route('/un-deploy')
def remove_client():
    return "<h1>REMOVING</h1>" # return HTML

# Set resource tresholds
@app.route('/thresholds')
def remove_client():
    return "<h1>REMOVING</h1>" # return HTML


app.run(host="0.0.0.0", port=5000, debug=True)