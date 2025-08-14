import sqlite3

con = sqlite3.connect("monitoring-orchestrator.db")
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Thresholds (
        threshold_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpu_percentage INTEGER,
        mem_percentage INTEGER,
        disk_percentage INTEGER
    );'''
)

cur.execute('''
    CREATE TABLE IF NOT EXISTS Status (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        isDeployed INTEGER,
        os TEXT,
        cpu_cores INTEGER,
        total_mem INTEGER,
        total_disk INTEGER
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Credentials (
        credentials_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        identity_keys TEXT
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Metrics (
        metrics_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        cpu_usage_percentage INTEGER,
        memory_usage_percentage INTEGER,
        disk_usage_percentage INTEGER,
        remote_id INTEGER,
        FOREIGN KEY (remote_id) REFERENCES Remotes(remote_id)
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Remotes (
        remote_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT,
        name TEXT,
        threshold_id INTEGER,
        credential_id INTEGER,
        status_id INTEGER,
        FOREIGN KEY (threshold_id) REFERENCES Thresholds(threshold_id),
        FOREIGN KEY (credential_id) REFERENCES Credentials(credentials_id),
        FOREIGN KEY (status_id) REFERENCES Status(status_id)
    );
''')

cur.execute('''
    SELECT name FROM sqlite_master WHERE type='table';
''')

print(cur.fetchall())

con.close()