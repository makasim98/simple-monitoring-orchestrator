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
