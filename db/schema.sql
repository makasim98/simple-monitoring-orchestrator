-- Drop tables if they exist to allow for re-initialization
DROP TABLE IF EXISTS Thresholds;
DROP TABLE IF EXISTS Status;
DROP TABLE IF EXISTS Credentials;
DROP TABLE IF EXISTS Metrics;
DROP TABLE IF EXISTS Remotes;

-- Create the required tables
CREATE TABLE Thresholds (
    threshold_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_percentage INTEGER,
    mem_percentage INTEGER,
    disk_percentage INTEGER
);

CREATE TABLE Status (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isDeployed INTEGER,
    os TEXT,
    cpu_cores INTEGER,
    total_mem INTEGER,
    total_disk INTEGER
);

CREATE TABLE Credentials (
    credentials_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    identity_keys TEXT
);

CREATE TABLE Metrics (
    metrics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_usage_percentage INTEGER,
    memory_usage_percentage INTEGER,
    disk_usage_percentage INTEGER,
    remote_id INTEGER,
    FOREIGN KEY (remote_id) REFERENCES Remotes(remote_id)
);

CREATE TABLE Remotes (
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