import sqlite3
from typing import Dict, Any
from services.db.db_init import get_db_connection  # Import the database connection function
from models.remote_server import Endpoint  # Import Endpoint from models folder

def add_endpoint(json_body: Dict[str, Any]) -> Endpoint:
    # Validate required fields
    required_fields = ['name', 'hostname', 'ssh_credentials']
    for field in required_fields:
        if field not in json_body:
            raise ValueError(f"Missing required field: {field}")

    ssh_credentials = json_body['ssh_credentials']
    if not isinstance(ssh_credentials, dict):
        raise ValueError("ssh_credentials must be a dictionary")
    if not ('password' in ssh_credentials or 'identity_file' in ssh_credentials):
        raise ValueError("ssh_credentials must contain either 'password' or 'identity_file'")

    # Create Endpoint object
    credentials = json_body['ssh_credentials']
    endpoint = Endpoint(
        name=json_body['name'],
        hostname=json_body['hostname'],
        username=credentials.get('user'),
        password=credentials.get('password', None),
        identity_file=credentials.get('identity_file', None),
        thresholds=json_body.get('thresholds', None)
    )

    # Save to SQLite database using get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the endpoint into the database tables
    cursor.execute(
        "INSERT INTO Thresholds (cpu_percentage, mem_percentage, disk_percentage) VALUES (?, ?, ?)",
        (endpoint.thresholds.cpu, endpoint.thresholds.memory, endpoint.thresholds.disk)
    )
    threshold_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO Credentials (ssh_user, ssh_pass, ssh_identity_file) VALUES (?, ?, ?)",
        (endpoint.username, endpoint.password, endpoint.identity_file.encode('utf-8') if endpoint.identity_file else None)
    )
    credentials_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO Status (is_deployed) VALUES (?)",
        (False,)
    )
    status_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO Remotes (name, hostname, credential_id, threshold_id, status_id) VALUES (?, ?, ?, ?, ?)",
        (endpoint.name, endpoint.hostname, credentials_id, threshold_id, status_id)
    )
    conn.commit()
    conn.close()

    return endpoint
