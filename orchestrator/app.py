from os import read
import sqlite3
from flask import Flask, jsonify, render_template_string, request
from services.configurator import add_remote, remove_remote, set_endpoint_thresholds
from services.scraper import init_scraper
from services.db.db_init import init_db, get_db_connection
from services.deployer import deploy_agent, remove_agent


# TODO: REMOVE LATER AFTER REFATORING
from models import Endpoint, Thresholds

app = Flask("Orchestrator")
init_db()
init_scraper()



monitored_endpoints = {}

# Function to load endpoints from the database
def load_endpoints_from_db():
    global monitored_endpoints
    monitored_endpoints = {}
    con = get_db_connection()
    cur = con.cursor()
    
    # Select all remote entries with their associated thresholds and credentials
    cur.execute('''
        SELECT 
            R.remote_id, R.hostname, R.name,
            C.ssh_user, C.ssh_pass, C.ssh_identity_file,
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
        remote_id, hostname, name, username, password, identity_file, cpu_threshold, memory_threshold, disk_threshold, is_deployed, timestamp, cpu_usage, memory_usage, disk_usage = row
        thresholds = Thresholds(cpu=cpu_threshold, memory=memory_threshold, disk=disk_threshold)
        monitored_endpoints[remote_id] = Endpoint(
            hostname=f"{hostname}:5000",
            name=name,
            username=username,
            password=password,
            identity_file=identity_file,
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

    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; width: 1000px; margin: 40px auto;">
    {% for endpoint_id, endpoint in monitored_endpoints.items() %}
 
            <a href="/info/{{ endpoint_id }}" style="text-decoration: none; color: black;">
                {% if endpoint.is_deployed %}
                <div style="background: #1DBC60; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center; padding: 4px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                    <p><strong>{{ endpoint.name }}</strong></p>
                    <p>CPU: {{ endpoint.cpu_usage }}%</p>
                    <p>Memory: {{ endpoint.memory_usage }}%</p>
                    <p>Disk: {{ endpoint.disk_usage }}%</p>
                    <p>Status: UP</p>
                </div>
                {% else %}
                <div style="background: #FF4C4C; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center; padding: 4px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                    <p><strong>{{ endpoint.name }}</strong></p>
                    <p>Status: DOWN</p>
                </div>
                {% endif %}
            </a>
   
    {% endfor %}
    </div>
    '''
    return render_template_string(html_template, monitored_endpoints=monitored_endpoints)

# Endpoint information page
@app.route('/info/<int:endpoint_id>')
def endpoint_info(endpoint_id):
    load_endpoints_from_db()
    endpoint = monitored_endpoints.get(endpoint_id)
    if not endpoint:
        return jsonify({"error": "Endpoint not found"}), 404

    return jsonify({
        "id": endpoint_id,
        "url": endpoint.url,
        "name": endpoint.name,
        "username": endpoint.username,
        "password": endpoint.password,
        "identity_keys": endpoint.identity_keys,
        "timestamp": endpoint.timestamp,
        "is_deployed": endpoint.is_deployed,
        "cpu_usage": endpoint.cpu_usage,
        "memory_usage": endpoint.memory_usage,
        "disk_usage": endpoint.disk_usage,
        "thresholds": {
            "cpu": endpoint.thresholds.cpu,
            "memory": endpoint.thresholds.memory,
            "disk": endpoint.thresholds.disk
        }
    })


# Get endpoints monitored by the Orchestrator
@app.route('/endpoints', methods=['GET'])
def get_endpoints():
    load_endpoints_from_db()

    endpoints_list = {}
    for endpoint_id, endpoint in monitored_endpoints.items():
        endpoints_list[endpoint_id] = {
            "name": endpoint.name,
            "url": endpoint.url,
            "is_deployed": endpoint.is_deployed
        }
    return jsonify(endpoints_list)


# -------------------- Endpoint Management Endpoints ----------------
@app.route('/add_endpoint', methods=['POST'])
def add_new_endpoint():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data was provided for the endpoint"}), 400
    try:
        endpoint = add_remote(data)
        return jsonify({"message": f"Endpoint '{endpoint.name}' added successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Remove existing Endpoint from the monitored APIs
@app.route('/remove_endpoint/<int:profile_id>', methods=['DELETE'])
def remove_endpoint(profile_id):
    try:
        remove_remote(profile_id)
        return jsonify({"message": f"Endpoint with ID {profile_id} removed successfully."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# ----------------------- Deployment Endpoints -----------------------
@app.route('/deploy/<int:profile_id>')
def deploy_remote_agent(profile_id):
    try:
        deploy_agent(profile_id)
        return jsonify({"message": f"Deployment successful for profile ID: {profile_id}"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# TODO: Implement actual removal logic
# Remove monitoring client from target remote server/vm
@app.route('/un-deploy/<int:profile_id>', methods=['DELETE'])
def remove_deployed_client(profile_id):
    try:
        remove_agent(profile_id)
        return jsonify({"message": f"Removal successful for profile ID: {profile_id}"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# --------------------- Thresholds Endpoints -----------------------
@app.route('/thresholds/<int:endpoint_id>', methods=['PUT'])
def set_thresholds(endpoint_id):
    try:
        new_thresholds = request.json
        if not new_thresholds:
            return jsonify({"error": "JSON Body cannot be empty!"}), 400
        endpoint_name = set_endpoint_thresholds(endpoint_id, new_thresholds)
        return jsonify({"message": f"Thresholds for endpoint '{endpoint_name}' updated successfully."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# --------------------- Start the Flask App -----------------------
app.run(host="0.0.0.0", port=5000, debug=True)