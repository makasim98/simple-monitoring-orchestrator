from .db_init import get_db_connection

def get_deployment_profiles():
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("""
        SELECT * 
        FROM Remotes AS R      
        INNER JOIN Status AS S ON R.status_id = S.status_id
        INNER JOIN Thresholds AS T ON R.threshold_id = T.threshold_id
    """)
    profiles = curs.fetchall()
    conn.close()
    return profiles


def get_deployment_profile(profile_id: int):
    conn = get_db_connection()
    curs = conn.cursor()   
    curs.execute("""
        SELECT R.hostname, C.ssh_user, C.ssh_pass, C.ssh_identity_file
        FROM Remotes as R
        INNER JOIN Credentials as C ON R.credential_id = C.credentials_id
        WHERE remote_id = ?
    """, (profile_id,))
    deploy_profile = curs.fetchone() 
    conn.close() 
    return deploy_profile


def save_deployment_metrics(profile_id: int, metrics: dict):
    conn = get_db_connection()
    curs = conn.cursor() 
    curs.execute("""
        INSERT INTO Metrics (remote_id, cpu_usage_percentage, memory_usage_percentage, disk_usage_percentage)
        VALUES (?, ?, ?, ?)
    """, (profile_id, metrics['cpu_percent'], metrics['mem_percent'], metrics['disk_percent']))
    conn.commit()
    conn.close()

def update_host_status(status_id: int, state: str, info=None):
    conn = get_db_connection()
    curs = conn.cursor()

    if state == "UP" and info is not None:
        curs.execute("""
            UPDATE Status
            SET state = ?, os = ?, cpu_cores = ?, total_memory = ?, total_disk = ?
            WHERE status_id = ?
        """, (state, info['os'], info['cpu_cores'], info['total_memory_bytes'], info['total_disk_bytes'], status_id))
    else:
        curs.execute("UPDATE Status SET state = ? WHERE status_id = ?", (state, status_id))
    conn.commit()
    conn.close()

def update_deployment_status(status_id: int, isDeployed: bool):
    if not isDeployed:
        update_host_status(status_id, "UNKNOWN", None)
    conn = get_db_connection()
    curs = conn.cursor()
    curs.execute("UPDATE Status SET is_deployed = ? WHERE status_id = ?", (isDeployed, status_id))
    conn.commit()
    conn.close()