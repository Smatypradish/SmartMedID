import psycopg2
import numpy as np
import pickle
import os
from cryptography.fernet import Fernet

# --- CONFIGURATION: Use environment variables! ---
DB_NAME = "SmartMedID_DB"
DB_USER = "postgres"
DB_PASS = "1234"  
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Establishes and returns a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error:
        return None

def face_to_binary(encoding_np):
    """Converts a face_recognition encoding (numpy array of floats) to a binary byte array."""
    if encoding_np is None:
        return None
    return pickle.dumps(encoding_np)

def binary_to_face(binary_data):
    """Converts a binary blob from the DB back to a face encoding (numpy array)."""
    if binary_data:
        return pickle.loads(binary_data)
    return None

# --- ENCRYPTION KEY MANAGEMENT ---

KEY_FILE = "secret.key"
FERNET_OBJ = None

def init_fernet():
    global FERNET_OBJ
    key = None
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as kf:
            kf.write(key)
    else:
        with open(KEY_FILE, "rb") as kf:
            key = kf.read()
    FERNET_OBJ = Fernet(key)

try:
    init_fernet()
except Exception:
    pass
