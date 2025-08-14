from os import read
from flask import Flask, jsonify, render_template_string, request

app = Flask("Orchestrator")

monitored_endpoints = {}

# Define the Endpoint class to manage monitored endpoints
class Thresholds:
    def __init__(self, cpu=80, memory=90, disk=80):
        self.cpu = cpu
        self.memory = memory
        self.disk = disk

class Endpoint:
    def __init__(self, url, name, username, password, thresholds=Thresholds()):
        self.url = url
        self.name = name
        self.username = username
        self.password = password
        self.is_deployed = False
        self.thresholds = Thresholds()

@app.route('/')
def dashboard():
    # Render the dashboard with monitored endpoints
    html_template = '''
    <h1>Orchestrator Dashboard</h1>
    <p>Manage your monitored endpoints here.</p>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; width: 400px; margin: 40px auto;">
        {% for box in monitored_endpoints %}
        <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">{{ box }}</div>
        {% endfor %}
    </div>
    '''
    return render_template_string(html_template, monitored_endpoints=monitored_endpoints.items())


# Get endpoints monitored by the Orchestrator
@app.route('/endpoints', methods=['GET'])
def get_endpoints():
    return jsonify(monitored_endpoints)


# ADD New Endpoint to the monitored APIs
@app.route('/add_endpoint/<path:URL>', methods=['POST'])
def add_endpoint(URL):
    data = request.json

    # Check for valid JSON data
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Extract data from JSON with safe defaults
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')

    # Validate required fields
    if not name:
        return jsonify({"error": "Name field is required"}), 400

    # Create a new Endpoint instance and add it to the dictionary
    monitored_endpoints[URL] = Endpoint(
        url=URL,
        name=name,
        username=username,
        password=password
    )

    return jsonify({"message": f"Endpoint '{name}' added successfully would you like to deploy it?"}), 201


# Remove existing Endpoint from the monitored APIs
@app.route('/remove_endpoint/<URL>', methods=['DELETE'])
def remove_endpoint(URL):
    if URL in monitored_endpoints:
        del monitored_endpoints[URL]
        return "<h1>REMOVING</h1>" # return HTML
    return "<h1>NOT FOUND</h1>", 404

# Deploy monitoring client to target remote server/vm
@app.route('/deploy')
def deploy_client():
    return "<h1>DEPLOYING</h1>" # return HTML

# Remove monitoring client from target remote server/vm
@app.route('/un-deploy/<URL>')
def remove_client(URL):
    return "<h1>UN-DEPLOYING</h1>" # return HTML

# Set resource thresholds
@app.route('/thresholds/<URL>', methods=['POST'])
def set_thresholds(URL):
    if URL not in monitored_endpoints:
        return jsonify({"error": "Endpoint not found"}), 404

    # Get the new thresholds from the request
    new_thresholds = request.json
    monitored_endpoints[URL].cpu_threshold = new_thresholds.get("cpu", monitored_endpoints[URL].cpu_threshold)
    monitored_endpoints[URL].memory_threshold = new_thresholds.get("memory", monitored_endpoints[URL].memory_threshold)
    monitored_endpoints[URL].disk_threshold = new_thresholds.get("disk", monitored_endpoints[URL].disk_threshold)

    return "<h1>SET THRESHOLDS</h1>" # return HTML



app.run(host="0.0.0.0", port=5000, debug=True)