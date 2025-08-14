from os import read
from flask import Flask, jsonify, render_template_string, request
from scraper import init_scraper
import sqlite3

app = Flask("Orchestrator")
init_scraper()

monitored_endpoints = {}

# Define the Endpoint class to manage monitored endpoints
class Thresholds:
    def __init__(self, cpu=80, memory=90, disk=80):
        self.cpu = cpu
        self.memory = memory
        self.disk = disk

class Endpoint:
    def __init__(
            self, url, name, username, password, identity_keys,
            is_deployed, timestamp, cpu_usage, memory_usage, disk_usage, thresholds=Thresholds()):
        self.url = url
        self.name = name
        self.username = username
        self.password = password
        self.identity_keys = identity_keys
        self.is_deployed = is_deployed
        self.thresholds = thresholds
        self.timestamp = timestamp
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.disk_usage = disk_usage


# Function to load endpoints from the database
def load_endpoints_from_db():
    global monitored_endpoints
    monitored_endpoints = {}
    con = sqlite3.connect("monitoring-orchestrator.db")
    cur = con.cursor()
    
    # Select all remote entries with their associated thresholds and credentials
    cur.execute('''
        SELECT 
            R.remote_id, R.hostname, R.name,
            C.username, C.password, C.identity_keys,
            T.cpu_percentage, T.mem_percentage, T.disk_percentage,
            S.isDeployed,
            MAX(M.timestamp), M.cpu_usage_percentage, M.memory_usage_percentage, M.disk_usage_percentage
        FROM Remotes AS R
        LEFT JOIN Credentials AS C ON R.credential_id = C.credentials_id
        LEFT JOIN Thresholds AS T ON R.threshold_id = T.threshold_id
        LEFT JOIN Status AS S ON R.status_id = S.status_id
        LEFT JOIN Metrics AS M ON R.remote_id = M.remote_id
        GROUP BY R.remote_id
    ''')
    
    endpoints_data = cur.fetchall()
    
    for row in endpoints_data:
        remote_id, hostname, name, username, password, identity_keys, cpu_threshold, memory_threshold, disk_threshold, is_deployed, timestamp, cpu_usage, memory_usage, disk_usage = row
        thresholds = Thresholds(cpu=cpu_threshold, memory=memory_threshold, disk=disk_threshold)
        monitored_endpoints[remote_id] = Endpoint(
            url=f"{hostname}:5000",
            name=name,
            username=username,
            password=password,
            identity_keys=identity_keys,
            thresholds=thresholds,
            is_deployed=bool(is_deployed),
            timestamp=timestamp,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage
        )
    
    con.close()

@app.route('/')
def dashboard():
    
    load_endpoints_from_db()  # Load endpoints from the database
    # Render the dashboard with monitored endpoints
    html_template = '''
    <h1>Orchestrator Dashboard</h1>
    <p>Manage your monitored endpoints here.</p>

    {% for endpoint_id, endpoint in monitored_endpoints.items() %}
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; width: 600px; margin: 40px auto;">
            <a href="/info/{{ endpoint_id }}" style="text-decoration: none; color: black;">
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center; padding: 4px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                    <p><strong>{{ endpoint.name }}</strong></p>
                    <p>CPU: {{ endpoint.cpu_usage }}%</p>
                    <p>Memory: {{ endpoint.memory_usage }}%</p>
                    <p>Disk: {{ endpoint.disk_usage }}%</p>
                </div>
            </a>
        </div>
    {% endfor %}
    '''
    return render_template_string(html_template, monitored_endpoints=monitored_endpoints)

# Endpoint information page
@app.route('/info/<int:endpoint_id>')
def endpoint_info(endpoint_id):
    endpoint = monitored_endpoints.get(endpoint_id)
    if not endpoint:
        return jsonify({"error": "Endpoint not found"}), 404

    return jsonify({
        "id": endpoint_id,
        "url": endpoint.url,
        "name": endpoint.name,
        "username": endpoint.username,
        "password": endpoint.password,
        "thresholds": {
            "cpu": endpoint.thresholds.cpu,
            "memory": endpoint.thresholds.memory,
            "disk": endpoint.thresholds.disk
        }
    })


# Get endpoints monitored by the Orchestrator
@app.route('/endpoints', methods=['GET'])
def get_endpoints():
    return jsonify(monitored_endpoints)


# ADD New Endpoint to the monitored APIs
@app.route('/add_endpoint/<path:url>', methods=['POST'])
def add_endpoint(url):
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
    monitored_endpoints[url] = Endpoint(
        url=url,
        name=name,
        username=username,
        password=password
    )

    return jsonify({"message": f"Endpoint '{name}' added successfully would you like to deploy it?"}), 201


# Remove existing Endpoint from the monitored APIs
@app.route('/remove_endpoint/<url>', methods=['DELETE'])
def remove_endpoint(url):
    if url in monitored_endpoints:
        del monitored_endpoints[url]
        return "<h1>REMOVING</h1>" # return HTML
    return "<h1>NOT FOUND</h1>", 404

# Deploy monitoring client to target remote server/vm
@app.route('/deploy')
def deploy_client():
    return "<h1>DEPLOYING</h1>" # return HTML

# Remove monitoring client from target remote server/vm
@app.route('/un-deploy/<url>')
def remove_client(url):
    return "<h1>UN-DEPLOYING</h1>" # return HTML

# Set resource thresholds
@app.route('/thresholds/<url>', methods=['POST'])
def set_thresholds(url):
    if url not in monitored_endpoints:
        return jsonify({"error": "Endpoint not found"}), 404

    # Get the new thresholds from the request
    new_thresholds = request.json
    monitored_endpoints[url].cpu_threshold = new_thresholds.get("cpu", monitored_endpoints[url].cpu_threshold)
    monitored_endpoints[url].memory_threshold = new_thresholds.get("memory", monitored_endpoints[url].memory_threshold)
    monitored_endpoints[url].disk_threshold = new_thresholds.get("disk", monitored_endpoints[url].disk_threshold)

    return "<h1>SET THRESHOLDS</h1>" # return HTML



app.run(host="0.0.0.0", port=5000, debug=True)