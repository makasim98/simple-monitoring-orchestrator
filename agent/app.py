from flask import Flask, request, jsonify

app = Flask("ovserver-agent")

# Get status of the machine
@app.route('/status')
def status():
    return jsonify

# Retrieve metrics from the machine
@app.route('/metrics', methods=['GET'])
def metrics():
    return "<h1>Orchestrator Dashboard!!!</h1>" # return HTML



app.run(host="0.0.0.0", port=5000, debug=True)