-- Create the required tables
CREATE TABLE Thresholds (
    remote_id INTEGER PRIMARY KEY,
    cpu_percentage DECIMAL(5, 2) NOT NULL,
    mem_percentage DECIMAL(5, 2) NOT NULL,
    disk_percentage DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (remote_id) REFERENCES Remotes(remote_id)
);

CREATE TABLE Status (
    remote_id INTEGER PRIMARY KEY,
    is_deployed BOOLEAN NOT NULL DEFAULT 0,
    state VARCHAR(10) NOT NULL DEFAULT 'UNKNOWN',
    os VARCHAR(10),
    cpu_cores INTEGER,
    total_mem INTEGER,
    total_disk INTEGER,
    FOREIGN KEY (remote_id) REFERENCES Remotes(remote_id)
);

CREATE TABLE Credentials (
    remote_id INTEGER PRIMARY KEY,
    ssh_user VARCHAR(50) NOT NULL,
    ssh_pass VARCHAR(50),
    ssh_identity_file BLOB,
    /* CHECK (
        (ssh_pass IS NOT NULL AND ssh_pass != '') 
        OR 
        (ssh_identity_file IS NOT NULL AND ssh_identity_file != '')
    ), */
    FOREIGN KEY (remote_id) REFERENCES Remotes(remote_id)
);

CREATE TABLE Remotes (
    remote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    hostname VARCHAR(100) NOT NULL
);

CREATE TABLE Metrics (
    metrics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_usage_percentage DECIMAL(5, 2) NOT NULL,
    memory_usage_percentage DECIMAL(5, 2) NOT NULL,
    disk_usage_percentage DECIMAL(5, 2) NOT NULL,
    remote_id INTEGER NOT NULL,
    FOREIGN KEY (remote_id) REFERENCES Remotes(remote_id)
);