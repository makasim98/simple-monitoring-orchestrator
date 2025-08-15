import sqlite3
from typing import Dict, Any
from services.db.db_init import get_db_connection  # Import the database connection function
from models.remote_server import Endpoint  # Import Endpoint from models folder

def add_remote(json_body: Dict[str, Any]) -> Endpoint:
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
    try:
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
        return endpoint
    except sqlite3.Error as e:
        conn.rollback()  
        raise
    finally:
        conn.close()

    
def remove_remote(profile_id: int):
    # Validate profile_id
    if not isinstance(profile_id, int) or profile_id <= 0:
        raise ValueError("Invalid profile_id. It must be a positive integer.")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        endpoint = conn.execute(
            "SELECT status_id, credential_id, threshold_id FROM Remotes WHERE remote_id = ?",
            (profile_id,)
        ).fetchone()

        if not endpoint:
            raise Exception(f"Error: Endpoint with ID {profile_id} not found.")

        status = conn.execute(
            "SELECT is_deployed FROM Status WHERE status_id = ?",
            (endpoint['status_id'],)
        ).fetchone()

        if status and status['is_deployed']:
            raise Exception(f"Cannot remove endpoint {profile_id}. The monitoring agent is currently deployed.")
            

        # Delete the endpoint and associated data from all tables  
        cursor.execute("DELETE FROM Metrics WHERE remote_id = ?", (profile_id,))
        cursor.execute("DELETE FROM Remotes WHERE remote_id = ?", (profile_id,))
        cursor.execute("DELETE FROM Thresholds WHERE threshold_id = ?", (endpoint['threshold_id'],))
        cursor.execute("DELETE FROM Credentials WHERE credentials_id = ?", (endpoint['credential_id'],))
        cursor.execute("DELETE FROM Status WHERE status_id = ?", (endpoint['status_id'],))
        conn.commit()
        print(f"Endpoint {profile_id} and all associated data have been removed.")
    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes if an error occurs
        raise  # Re-raise the exception after rollback
    finally:
        conn.close()


def set_endpoint_thresholds(endpoint_id: int, new_thresholds: Dict[str, Any]):
    if not isinstance(endpoint_id, int) or endpoint_id <= 0:
        raise ValueError("Invalid endpoint_id. It must be a positive integer.")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT R.name, T.threshold_id
            FROM Thresholds T
            INNER JOIN Remotes R ON T.threshold_id = R.threshold_id
            WHERE remote_id = ?
        """, (endpoint_id,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"Endpoint with ID {endpoint_id} not found.")

        required_fields = ['cpu', 'memory', 'disk']
        for field in required_fields:
            if field not in new_thresholds:
                raise ValueError(f"Missing required field: {field}")
            if new_thresholds[field] is None or (not isinstance(new_thresholds[field], float) or new_thresholds[field] < 0.0 or new_thresholds[field] > 100.0):
                raise ValueError(f"Invalid value for {field}. It must be a float between 0.0 and 100.0.")

        cpu = new_thresholds.get('cpu')
        memory = new_thresholds.get('memory')
        disk = new_thresholds.get('disk')

        cursor.execute(
            "UPDATE Thresholds SET cpu_percentage = ?, mem_percentage = ?, disk_percentage = ? WHERE threshold_id = ?",
            (cpu, memory, disk, result['threshold_id'])
        )
        conn.commit()
        return result['name']
    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes if an error occurs
        raise
    finally:
        conn.close()