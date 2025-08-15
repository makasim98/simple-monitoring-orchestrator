from flask import Flask, request, jsonify
from metrics import get_sys_metrics, get_system_info

app = Flask("observer-agent")

# Get status of the machine
@app.route('/status', methods=['GET'])
def status():
    try:
        sys_info = get_system_info()
        return jsonify(sys_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve metrics from the machine
@app.route('/metrics', methods=['GET'])
def metrics():
    try:
        metrics_data = get_sys_metrics()
        return jsonify(metrics_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



app.run(host="0.0.0.0", port=5000, debug=True)