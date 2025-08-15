import os
import sqlite3

# Define the paths for your database and schema files
DATABASE_FILE = './orchestrator/services/db/orchestrator.db'
SCHEMA_FILE = './orchestrator/services/db/schema.sql'

def init_db():
    if not os.path.exists(DATABASE_FILE):
        print(f"Database file '{DATABASE_FILE}' not found. Initializing...")
        try:
            # Create a connection to the new database file
            conn = sqlite3.connect(DATABASE_FILE)
            
            # Read and execute the schema file
            with open(SCHEMA_FILE, 'r') as f:
                conn.executescript(f.read())
            
            conn.close()
            print("Database initialized successfully.")
        except FileNotFoundError:
            print(f"Error: Schema file '{SCHEMA_FILE}' not found. Cannot initialize database.")
            # Clean up the newly created, but empty, database file
            if os.path.exists(DATABASE_FILE):
                os.remove(DATABASE_FILE)
            raise
    else:
        print("Database file already exists. Skipping initialization.")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    # Configure the connection to return rows that behave like dictionaries
    conn.row_factory = sqlite3.Row
    return conn

