from .db_init import get_db_connection

def get_deployment_profile(profile_id: int):
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute("""
        SELECT R.hostname, C.ssh_user, C.ssh_pass, C.ssh_identity_file
        FROM Remotes as R
        INNER JOIN Credentials as C ON R.credential_id = C.credentials_id
        WHERE remote_id = ?
    """, (profile_id,))
    deploy_profile = cur.fetchone() 
    con.close()
    
    return deploy_profile

def update_deployment_status(profile_id: int, isDeployed: bool):
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute("""
        UPDATE Status
        SET is_deployed = ?
        WHERE status_id = (
            SELECT status_id
            FROM Remotes
            WHERE remote_id = ?
        )
    """, (isDeployed, profile_id))
    
    con.commit()
    con.close()