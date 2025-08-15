-- Drop tables if they exist to allow for re-initialization
DROP TABLE IF EXISTS Thresholds;
DROP TABLE IF EXISTS Status;
DROP TABLE IF EXISTS Credentials;
DROP TABLE IF EXISTS Metrics;
DROP TABLE IF EXISTS Remotes;

-- Create the required tables
CREATE TABLE Thresholds (
    threshold_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_percentage DECIMAL(5, 2) NOT NULL,
    mem_percentage DECIMAL(5, 2) NOT NULL,
    disk_percentage DECIMAL(5, 2) NOT NULL
);

CREATE TABLE Status (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_deployed BOOLEAN NOT NULL DEFAULT 0,
    os VARCHAR(10),
    cpu_cores INTEGER,
    total_mem INTEGER,
    total_disk INTEGER
);

CREATE TABLE Credentials (
    credentials_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ssh_user VARCHAR(50) NOT NULL,
    ssh_pass VARCHAR(50),
    ssh_identity_file BLOB,
    CHECK (
        (ssh_pass IS NOT NULL AND ssh_pass != '') 
        OR 
        (ssh_identity_file IS NOT NULL AND ssh_identity_file != '')
    )
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

CREATE TABLE Remotes (
    remote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    hostname VARCHAR(100) NOT NULL,
    threshold_id INTEGER NOT NULL,
    credential_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    FOREIGN KEY (threshold_id) REFERENCES Thresholds(threshold_id),
    FOREIGN KEY (credential_id) REFERENCES Credentials(credentials_id),
    FOREIGN KEY (status_id) REFERENCES Status(status_id)
);