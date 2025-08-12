from flask import Flask, request, jsonify
from metrics import gather_metrics, get_sysinfo

app = Flask("observer-agent")

# Get status of the machine
@app.route('/status', methods=['GET'])
def status():
    return jsonify(get_sysinfo())

# Retrieve metrics from the machine
@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(gather_metrics())

app.run(host="0.0.0.0", port=5000, debug=True)