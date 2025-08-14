import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the database
con = sqlite3.connect("db/monitoring-database.db")
cur = con.cursor()

# --- Insert 5 rows into Thresholds table ---
print("Inserting data into Thresholds table...")
thresholds_data = [
    (80, 90, 85),
    (75, 80, 70),
    (90, 95, 90),
    (70, 75, 65),
    (85, 88, 80)
]
for cpu, mem, disk in thresholds_data:
    cur.execute("INSERT INTO Thresholds (cpu_percentage, mem_percentage, disk_percentage) VALUES (?, ?, ?)", (cpu, mem, disk))
con.commit()

# --- Insert 5 rows into Status table ---
print("Inserting data into Status table...")
status_data = [
    (1, "Linux", 4, 16384, 1024000),
    (1, "Windows", 8, 32768, 2048000),
    (0, "Linux", 2, 8192, 512000),
    (1, "Macos", 6, 24576, 1536000),
    (0, "Linux", 4, 16384, 1024000)
]
for is_deployed, os, cpu_cores, total_mem, total_disk in status_data:
    cur.execute("INSERT INTO Status (isDeployed, os, cpu_cores, total_mem, total_disk) VALUES (?, ?, ?, ?, ?)", (is_deployed, os, cpu_cores, total_mem, total_disk))
con.commit()

# --- Insert 5 rows into Credentials table ---
print("Inserting data into Credentials table...")
credentials_data = [
    ("user1", "pass123", "keyA"),
    ("admin", "adminpass", "keyB"),
    ("guest", "guestpass", "keyC"),
    ("user4", "securepass", "keyD"),
    ("user5", "anotherpass", "keyE")
]
for username, password, keys in credentials_data:
    cur.execute("INSERT INTO Credentials (username, password, identity_keys) VALUES (?, ?, ?)", (username, password, keys))
con.commit()

# --- Insert 5 rows into Remotes table ---
print("Inserting data into Remotes table...")
remotes_data = [
    ("http://prod.api.com", "Production API", 1, 1, 1),
    ("http://dev.web.org", "Development Web", 2, 2, 2),
    ("http://qa.test.net", "QA Test", 3, 3, 3),
    ("http://app.server.io", "Application Server", 4, 4, 4),
    ("http://db.server.co", "Database Server", 5, 5, 5)
]
for hostname, name, threshold_id, credential_id, status_id in remotes_data:
    cur.execute("INSERT INTO Remotes (hostname, name, threshold_id, credential_id, status_id) VALUES (?, ?, ?, ?, ?)", (hostname, name, threshold_id, credential_id, status_id))
con.commit()

# --- Insert 10 rows into Metrics table (2 per remote_id) ---
print("Inserting data into Metrics table...")
for remote_id in range(1, 6):
    for i in range(2):
        # Generate some random, but plausible metrics
        cpu = random.randint(10, 99)
        mem = random.randint(20, 95)
        disk = random.randint(30, 99)
        
        # Set a timestamp for each metric
        timestamp = datetime.now() - timedelta(minutes=i)
        
        cur.execute("INSERT INTO Metrics (timestamp, cpu_usage_percentage, memory_usage_percentage, disk_usage_percentage, remote_id) VALUES (?, ?, ?, ?, ?)", (timestamp, cpu, mem, disk, remote_id))
con.commit()

# Close the connection
con.close()
print("\n\nDatabase populated successfully!\n\n")