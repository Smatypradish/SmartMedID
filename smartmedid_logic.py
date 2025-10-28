import hashlib
from datetime import datetime
import psycopg2.errors
import time
import random

# Optional CV/ML libraries
try:
    import cv2, face_recognition
except ImportError:
    cv2 = None
    face_recognition = None

from db_utils import get_db_connection, face_to_binary, binary_to_face, FERNET_OBJ

# --- Anomaly Detection Framework ---
try:
    import pandas as pd
    from sklearn.ensemble import IsolationForest
except ImportError:
    pd, IsolationForest = None, None

def check_for_anomalies():
    """Identifies anomalous failed login patterns."""
    if IsolationForest is None:
        return "ML libraries not installed for Anomaly Detection."
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed for anomaly detection."
    log_query = "SELECT time, doctor_id, reason FROM AccessLogs WHERE status = 'FAIL' and reason != 'Invalid password';"
    try:
        df = pd.read_sql(log_query, conn)
    except Exception as e:
        return f"Error loading log data: {e}"
    finally:
        conn.close()
    if df.empty or len(df) < 20: 
        return "Insufficient failed login data for anomaly detection (min 20 needed)."
    df['hour'] = df['time'].dt.hour
    df['dayofweek'] = df['time'].dt.dayofweek
    df['doctor_id_encoded'] = df['doctor_id'].astype('category').cat.codes
    features = df[['hour', 'dayofweek', 'doctor_id_encoded']]
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)
    df['anomaly'] = model.predict(features)
    anomalies = df[df['anomaly'] == -1]
    if not anomalies.empty:
        return f"🚨 SECURITY ALERT: {len(anomalies)} anomalous login failures detected. Check logs."
    else:
        return "Anomaly check complete. No suspicious login patterns found."

# --- Core Logic Functions ---

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log_access(doc_id, patient_id, status, reason=""):
    conn = get_db_connection()
    if conn is None:
        return
    insert_query = """
    INSERT INTO AccessLogs (time, doctor_id, patient_id, status, reason)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, 
                        (datetime.now(), doc_id, patient_id, status, reason))
            conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()

def enroll_doctor_db(doc_id, password, email, face_encoding_np):
    conn = get_db_connection()
    if conn is None:
        return False, "Database connection failed."
    hashed_pw = hash_password(password)
    face_binary = face_to_binary(face_encoding_np)

    insert_query = """
    INSERT INTO Doctors (doctor_id, password_hash, email, face_encoding)
    VALUES (%s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, (doc_id, hashed_pw, email, face_binary))
            conn.commit()
            return True, f"Doctor '{doc_id}' enrolled successfully into DB."
    except psycopg2.errors.UniqueViolation:
        return False, "Error: Doctor ID or Email already exists."
    except Exception as e:
        conn.rollback()
        return False, f"Database enrollment error: {e}"
    finally:
        conn.close()

def get_doctor_auth_data(doc_id):
    conn = get_db_connection()
    if conn is None:
        return None
    select_query = """
    SELECT password_hash, email, face_encoding
    FROM Doctors
    WHERE doctor_id = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(select_query, (doc_id,))
            result = cur.fetchone()
            if result is None:
                return None
            password_hash, email, face_binary = result
            face_encoding_np = binary_to_face(face_binary)
            return {
                "password_hash": password_hash,
                "email": email,
                "face_encoding": face_encoding_np
            }
    except Exception:
        return None
    finally:
        conn.close()

def enroll_patient_db(pid, name, dob, condition, email, date_str, face_encoding_np):
    conn = get_db_connection()
    if conn is None or FERNET_OBJ is None:
        return False, "DB or Encryption Key unavailable."
    record = f"ID: {pid}, Name: {name}, DOB: {dob}, Condition: {condition}, Date: {date_str}, Email: {email}"
    encrypted_record = FERNET_OBJ.encrypt(record.encode())
    face_binary = face_to_binary(face_encoding_np)
    insert_query = """
    INSERT INTO Patients (patient_id, encrypted_record, email, face_encoding)
    VALUES (%s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, (pid, encrypted_record, email, face_binary))
            conn.commit()
            return True, f"Patient '{pid}' enrolled successfully."
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False, "Error: Patient ID or Email already exists."
    except Exception as e:
        conn.rollback()
        return False, f"Database enrollment error: {e}"
    finally:
        conn.close()

def get_patient_data_for_mfa():
    conn = get_db_connection()
    if conn is None:
        return {}
    select_query = "SELECT patient_id, face_encoding, encrypted_record FROM Patients;"
    face_db = {}
    try:
        with conn.cursor() as cur:
            cur.execute(select_query)
            for pid, face_binary, encrypted_record in cur.fetchall():
                face_db[pid] = {
                    "face_encoding": binary_to_face(face_binary),
                    "encrypted_record": encrypted_record
                }
            return face_db
    except Exception:
        return {}
    finally:
        conn.close()

def decrypt_patient_record(encrypted_record):
    if FERNET_OBJ is None:
        return None, "Encryption Key unavailable."
    try:
        if not isinstance(encrypted_record, bytes):
            encrypted_record = bytes(encrypted_record)
    except Exception as e:
        return None, f"Decryption failed: Token is invalid type ({type(encrypted_record)})"
    try:
        decrypted_bytes = FERNET_OBJ.decrypt(encrypted_record)
        return decrypted_bytes.decode(), None
    except Exception as e:
        return None, f"Decryption failed: {e}"

def get_patient_email(pid):
    conn = get_db_connection()
    if conn is None:
        return None
    select_query = "SELECT email FROM Patients WHERE patient_id = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(select_query, (pid,))
            result = cur.fetchone()
            return result[0] if result else None
    except Exception:
        return None
    finally:
        conn.close()

def get_patient_record_by_id(pid):
    conn = get_db_connection()
    if conn is None:
        return None
    select_query = "SELECT encrypted_record FROM Patients WHERE patient_id = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(select_query, (pid,))
            result = cur.fetchone()
            return result[0] if result else None
    except Exception:
        return None
    finally:
        conn.close()

def get_all_records_summary():
    conn = get_db_connection()
    if conn is None:
        return [], []
    doctors = []
    patients = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT doctor_id, email FROM Doctors;")
            doctors = [{"id": r[0], "contact": r[1]} for r in cur.fetchall()]
            cur.execute("SELECT patient_id, email FROM Patients;")
            patients = [{"id": r[0], "contact": r[1]} for r in cur.fetchall()]
        return doctors, patients
    except Exception:
        return [], []
    finally:
        conn.close()

def delete_record_db(typ, idv):
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            if typ == "Doctor":
                cur.execute("DELETE FROM Doctors WHERE doctor_id = %s;", (idv,))
            elif typ == "Patient":
                cur.execute("DELETE FROM Patients WHERE patient_id = %s;", (idv,))
            conn.commit()
            return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def get_all_logs():
    conn = get_db_connection()
    if conn is None:
        return []
    select_query = "SELECT time, doctor_id, patient_id, status, reason FROM AccessLogs ORDER BY time DESC;"
    logs = []
    try:
        with conn.cursor() as cur:
            cur.execute(select_query)
            for t, d, p, s, r in cur.fetchall():
                logs.append({
                    "time": t.strftime("%Y-%m-%d %H:%M:%S"),
                    "doctor": d,
                    "patient": p,
                    "status": s,
                    "reason": r
                })
        return logs
    except Exception:
        return []
    finally:
        conn.close()
