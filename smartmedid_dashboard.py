import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import os, random, smtplib, time, sys
from email.mime.text import MIMEText
from datetime import datetime
import tkinter.font as tkfont
import csv
import threading 

# --- DEPENDENCY IMPORTS (Wrapped in try/except for robustness) ---
try:
    from PIL import Image, ImageTk 
except ImportError:
    class DummyImage:
        @staticmethod
        def open(path): return DummyImage()
        def resize(self, w, h, resample): return self
    Image = DummyImage
    ImageTk = DummyImage

try:
    import speech_recognition as sr
except ImportError:
    sr = None
    
try:
    import cv2, face_recognition
    # OPTIONAL: Define custom camera backend for stability on Windows
    CAP_BACKEND = cv2.CAP_DSHOW 
except ImportError:
    cv2 = None
    face_recognition = None
    CAP_BACKEND = 0 # Default index if not using advanced features
# ------------------------------------------------------------------

# Import all core logic functions
from smartmedid_logic import (
    hash_password, log_access, enroll_doctor_db, get_doctor_auth_data,
    enroll_patient_db, get_patient_data_for_mfa, decrypt_patient_record,
    get_patient_email, get_patient_record_by_id, get_all_records_summary,
    delete_record_db, get_all_logs,
    check_for_anomalies
)

# --- 1. CONFIGURATION (CRITICAL) ---
GMAIL_SENDER = "smatypradish@gmail.com" 
GMAIL_APP_PASS = "ygha pjwm vebm bqnj" # <-- UPDATE YOUR GMAIL APP PASSWORD
MICROPHONE_INDEX = None 
OTP_EXPIRY_SECONDS = 60
OTP_STORE = {} 
TEXT_FONT = None 
BACKGROUND_IMAGE = None 

# --- 2. THEME DEFINITION (Refined Colors) ---
COLOR_PRIMARY_BLUE = "#1A5276"    # Darker professional blue
COLOR_SECONDARY_DARK = "#34495E"  # Dark gray text
COLOR_BACKGROUND_LIGHT = "#ECF0F1" # Light gray background
COLOR_HEADER_BG = "#2C3E50"       # Dark header
COLOR_ACCENT_SUCCESS = "#2ECC71" # Green
COLOR_ACCENT_DANGER = "#E74C3C"  # Red

# --- 3. WINDOW HELPERS & STYLING ---

def _fit_screen(root):
    """Sets initial window size and configures fonts and ttk styles."""
    
    root.state("zoomed")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    def_font = tkfont.nametofont("TkDefaultFont")
    def_font.config(size=max(10, int(h/90)), family="Helvetica") # Use Helvetica for modern look

    style = ttk.Style()
    style.theme_use("clam")
    
    # Base Styles
    style.configure("TLabel", background=COLOR_BACKGROUND_LIGHT, foreground=COLOR_SECONDARY_DARK, font=def_font)
    style.configure("TFrame", background=COLOR_BACKGROUND_LIGHT)

    # Treeview (Admin Panel Data)
    style.configure("Treeview", rowheight=max(25,int(h/45)), font=def_font, background="white", foreground=COLOR_SECONDARY_DARK, fieldbackground="white")
    style.map("Treeview", background=[('selected', COLOR_PRIMARY_BLUE)])
    style.configure("Treeview.Heading", font=(def_font.actual("family"), max(10,int(h/90)), "bold"), background=COLOR_HEADER_BG, foreground="white")
    
    # Notebook/Tabs (Admin Panel)
    style.configure("TNotebook", background=COLOR_BACKGROUND_LIGHT, borderwidth=0)
    style.configure("TNotebook.Tab", background="#BDC3C7", foreground=COLOR_SECONDARY_DARK, padding=[10, 5])
    style.map("TNotebook.Tab", background=[("selected", COLOR_PRIMARY_BLUE)], foreground=[("selected", "white")])

    # Button Styles
    style.configure("Primary.TButton", padding=(20, 10), font=("Helvetica", 11, "bold"), background=COLOR_PRIMARY_BLUE, foreground="white")
    style.map("Primary.TButton", background=[("active", "#1F618D"), ("pressed", "#154360")], foreground=[("active", "white")])
               
    style.configure("Accent.TButton", padding=(15, 8), font=("Helvetica", 10, "bold"), background=COLOR_ACCENT_DANGER, foreground="white")
    style.map("Accent.TButton", background=[("active", "#C0392B"), ("pressed", "#A93226")])
    
    style.configure("Success.TButton", padding=(15, 8), font=("Helvetica", 10, "bold"), background=COLOR_ACCENT_SUCCESS, foreground="white")
    style.map("Success.TButton", background=[("active", "#28B463"), ("pressed", "#1E8449")])


    return tkfont.Font(family="Helvetica", size=max(10, int(h/110)))

def center(win):
    """Centers a window on the screen."""
    win.update_idletasks()
    w = win.winfo_width(); h = win.winfo_height()
    sw = win.winfo_screenwidth(); sh = win.winfo_screenheight()
    x = (sw - w) // 2; y = (sh - h) // 2
    win.geometry(f"+{x}+{y}")

# --- 4. CAMERA & FACE LOGIC (Backend Fix Applied) ---

def capture_face(title, prompt):
    if cv2 is None or face_recognition is None:
        messagebox.showerror("Dependency", "OpenCV and face_recognition required.")
        return None
    
    # Using CAP_BACKEND fix
    cap = cv2.VideoCapture(0, CAP_BACKEND) 
    
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot open camera. Try closing all other video apps.")
        return None

    messagebox.showinfo(title, prompt)
    captured_encoding = None

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        
        box_color = (0, 0, 255) 
        if faces:
            box_color = (0, 255, 0)
            top, right, bottom, left = faces[0]
            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
            
        cv2.putText(frame, "Press SPACE to capture | Q to cancel", (8, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow(title, frame)
        
        k = cv2.waitKey(1) & 0xFF
        if k == ord(" "):
            if faces:
                encs = face_recognition.face_encodings(rgb, faces)
                if encs:
                    captured_encoding = encs[0]
                    break
            else:
                messagebox.showwarning("Capture", "No face detected.")
        elif k == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return captured_encoding

def authenticate_face_probe(timeout=8):
    if cv2 is None or face_recognition is None: return None
    
    face_db_data = get_patient_data_for_mfa() 
    if not face_db_data: return None

    # Using CAP_BACKEND fix
    cap = cv2.VideoCapture(0, CAP_BACKEND)
    if not cap.isOpened(): 
        messagebox.showerror("Camera Error", "Cannot open camera. Try closing all other video apps.")
        return None
    
    matched_pid = None
    start = time.time()
    
    while time.time() - start < timeout:
        ret, frame = cap.read()
        if not ret: break
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encs = face_recognition.face_encodings(rgb)
        
        if encs:
            probe = encs[0]
            for pid, data in face_db_data.items():
                stored = data.get("face_encoding")
                if stored is None: continue

                match = face_recognition.compare_faces([stored], probe, tolerance=0.55)[0] 
                if match:
                    matched_pid = pid
                    break 
        
        cv2.imshow("Patient Face Auth", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"): break
        if matched_pid: break 

    cap.release()
    cv2.destroyAllWindows()
    return matched_pid
    
# ==============================================================================
# --- VOICE VERIFICATION (Timeout set to 10 seconds) ---
# ==============================================================================
def patient_voice_verify(prompt_phrase="Health is Wealth", timeout=6): 
    """
    Performs voice verification. Timeout is 10 seconds.
    """
    if sr is None:
        messagebox.showerror("Dependency", "Speech recognition required. Ensure 'speech_recognition' and 'PyAudio' are installed.")
        return False
        
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
            messagebox.showinfo("Voice Verification", f"Say: '{prompt_phrase}'")
            r.adjust_for_ambient_noise(source, duration=0.7)
            
            messagebox.showinfo("Listening...", "Start speaking now (10 seconds).") 
            audio = r.listen(source, timeout=timeout, phrase_time_limit=timeout)
            
            try:
                text = r.recognize_google(audio)
                messagebox.showinfo("Recognition Result", f"Google heard: '{text}'") 
                
                return prompt_phrase.lower() in text.lower()
                
            except sr.UnknownValueError:
                messagebox.showerror("Voice Error", "Google Speech Recognition could not understand audio. Try speaking clearer.")
                return False
            except sr.RequestError as e:
                messagebox.showerror("Voice Error", f"Could not request results from Google Speech Recognition service; check internet connection: {e}")
                return False
            
    except Exception as e:
        messagebox.showerror("Voice Error", f"Voice verification failed (Microphone/System Error). Ensure PyAudio is installed: {e}")
        return False
# ==============================================================================
# --- END OF VOICE FIX ---
# ==============================================================================
        
# --- 5. CORE APPLICATION FLOWS ---

def generate_otp():
    """Generates a 6-digit random number for OTP."""
    return str(random.randint(100000, 999999))

def send_email_otp_to(recipient_email):
    """Generates an OTP, stores it, and sends it via email."""
    
    otp_code = generate_otp()
    expiry_time = time.time() + OTP_EXPIRY_SECONDS
    OTP_STORE[recipient_email] = {"otp": otp_code, "expiry": expiry_time}
    
    subject = "SmartMedID One-Time Password (OTP)"
    body = f"Your One-Time Password (OTP) is: {otp_code}\nIt will expire in {OTP_EXPIRY_SECONDS} seconds."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_SENDER
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_SENDER, recipient_email, msg.as_string())
        messagebox.showinfo("OTP Sent", f"OTP successfully sent to {recipient_email}")
        return True
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send OTP to {recipient_email}. Check GMAIL_APP_PASS and internet: {e}")
        return False

def check_otp_valid(recipient_email, entered_otp):
    """Checks the entered OTP against the stored one for validity and expiry."""
    
    stored_data = OTP_STORE.get(recipient_email)
    
    if not stored_data:
        return False, "No OTP generated for this email."
        
    if time.time() > stored_data["expiry"]:
        del OTP_STORE[recipient_email]
        return False, "OTP has expired."

    if stored_data["otp"] == entered_otp:
        del OTP_STORE[recipient_email] 
        return True, "Valid"
        
    return False, "Incorrect code."


def register_doctor():
    doc_id = simpledialog.askstring("Register Doctor", "Enter Doctor ID:")
    if not doc_id: return
    
    pwd = simpledialog.askstring("Register Doctor", "Enter password:", show="*")
    email = simpledialog.askstring("Register Doctor", "Enter doctor email (for OTP):")
    if not pwd or not email: return
    
    face_encoding = None # Doctor biometrics disabled
    
    success, message = enroll_doctor_db(doc_id, pwd, email, face_encoding)
    
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def register_patient():
    pid = simpledialog.askstring("Register Patient", "Enter Patient ID:")
    if not pid: return

    name = simpledialog.askstring("Register Patient", "Enter Name:")
    dob = simpledialog.askstring("Register Patient", "Enter Date of Birth (YYYY-MM-DD):")
    condition = simpledialog.askstring("Register Patient", "Enter Medical Condition:")
    patient_email = simpledialog.askstring("Register Patient", f"Enter e-mail for patient {pid}:")
    
    if not all([name, dob, condition, patient_email]):
        messagebox.showwarning("Incomplete", "All fields are required.")
        return
        
    date_str = datetime.now().strftime("%Y-%m-%d")

    face_encoding = capture_face("Patient Enrollment", "Look at camera to capture face.")
    if face_encoding is None:
        messagebox.showwarning("Enrollment Note", "Patient registration cancelled as face capture failed.")
        return

    success, message = enroll_patient_db(pid, name, dob, condition, patient_email, date_str, face_encoding)
    
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def doctor_login_with_otp(parent_win, doc_id, password):
    # Basic input validation
    if not doc_id or not password:
        messagebox.showwarning("Input Error", "Please enter both ID and Password.")
        return
        
    # 1. Password Check
    doctor_data = get_doctor_auth_data(doc_id)
    if not doctor_data:
        messagebox.showerror("Login", "Invalid Doctor ID.")
        return
        
    if doctor_data["password_hash"] != hash_password(password):
        log_access(doc_id, "N/A", "FAIL", "Invalid password")
        messagebox.showerror("Login", "Incorrect password.")
        return
        
    email = doctor_data.get("email")
    if not email:
        messagebox.showerror("Login", "No email on record for this doctor.")
        return

    # 2. OTP Delivery
    if not send_email_otp_to(email):
        return

    # 3. OTP Window
    otp_win = tk.Toplevel(parent_win)
    otp_win.title("Enter OTP")
    otp_win.grab_set() # Modal
    
    def submit_otp():
        entered = code_ent.get().strip()
        ok, reason = check_otp_valid(email, entered)
        
        if ok:
            messagebox.showinfo("Login", f"Doctor {doc_id} authenticated (Pass + OTP).")
            log_access(doc_id, "N/A", "SUCCESS", "Doctor login via Pass+OTP")
            otp_win.destroy()
            open_patient_access_window(doc_id)
        else:
            messagebox.showerror("OTP", f"OTP invalid: {reason}")
            
    tk.Label(otp_win, text=f"OTP sent to: {email}", bg=COLOR_BACKGROUND_LIGHT).pack(pady=6, padx=10)
    code_ent = ttk.Entry(otp_win); code_ent.pack(pady=6, padx=10)
    ttk.Button(otp_win, text="Submit", style="Primary.TButton", command=submit_otp).pack(pady=10)
    center(otp_win)


def patient_mfa_flow(doctor_id):
    # 1. Face Probe
    pid = authenticate_face_probe()
    if not pid:
        log_access(doctor_id, "Unknown", "FAIL", "Patient face not recognized")
        messagebox.showerror("Authentication", "Patient face not recognized. Access denied.")
        return
    
    # 2. Get Patient Email for OTP
    patient_email = get_patient_email(pid)
    if not patient_email:
        messagebox.showerror("Auth", "No e-mail on file for this patient.")
        return

    # 3. OTP to Patient
    if not send_email_otp_to(patient_email): return
    entered = simpledialog.askstring("Patient OTP", "Enter the OTP you received in Gmail:")
    ok, reason = check_otp_valid(patient_email, entered)
    
    if not ok:
        log_access(doctor_id, pid, "FAIL", f"Patient OTP invalid: {reason}")
        messagebox.showerror("Auth", f"Patient OTP invalid: {reason}")
        return

    # 4. Voice Verification
    if not patient_voice_verify():
        log_access(doctor_id, pid, "FAIL", "Voice verification failed")
        messagebox.showerror("Auth", "Voice verification failed. Access denied.")
        return

    # 5. Retrieve and Decrypt Record
    encrypted_record = get_patient_record_by_id(pid)
    record, error = decrypt_patient_record(encrypted_record)
    
    if record is None:
        log_access(doctor_id, pid, "FAIL", f"Decrypt failed: {error}")
        messagebox.showerror("Record", f"Decryption failed: {error}")
        return

    log_access(doctor_id, pid, "SUCCESS", "Face+OTP+Voice")
    show_decrypted_record(pid, record)

def emergency_override_flow(current_doc_id):
    # ... (Logic remains largely the same)
    pid = simpledialog.askstring("Emergency", "Enter Patient ID:")
    if not pid: return
    
    encrypted_record = get_patient_record_by_id(pid)
    if not encrypted_record:
        messagebox.showerror("Emergency", "Patient not found.")
        return
        
    primary_doc = simpledialog.askstring("Emergency", "Enter Primary Doctor ID:")
    primary_doc_data = get_doctor_auth_data(primary_doc)
    
    if not primary_doc_data:
        messagebox.showerror("Emergency", "Primary doctor not found.")
        return
        
    email = primary_doc_data.get("email")
    if not email:
        messagebox.showerror("Emergency", "Primary doctor has no email.")
        return
    
    if not send_email_otp_to(email): return
    
    messagebox.showinfo("Emergency", f"Emergency OTP sent to primary doctor {primary_doc}. Obtain and enter code.")
    entered = simpledialog.askstring("Emergency OTP", "Enter OTP received by primary doctor:")
    ok, reason = check_otp_valid(email, entered)
    
    if not ok:
        log_access(current_doc_id, pid, "FAIL", "Emergency OTP invalid")
        messagebox.showerror("Emergency", f"Emergency OTP invalid: {reason}")
        return
    
    record, error = decrypt_patient_record(encrypted_record)
    
    if record is None:
        messagebox.showerror("Emergency", f"Decrypt failed: {error}")
        return
        
    log_access(current_doc_id, pid, "SUCCESS", f"Emergency override by {primary_doc}")
    show_decrypted_record(pid, record)

# --- 6. GUI WINDOWS (Enhanced Layouts) ---

def show_decrypted_record(pid, record):
    w = tk.Toplevel(root)
    w.title(f"Patient Record: {pid}")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)
    w.grab_set()

    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text=f"Patient Record: {pid}", bg=COLOR_HEADER_BG, fg="white", font=("Helvetica", 16, "bold"), pady=10).pack(fill="x", padx=10)
    
    txt = scrolledtext.ScrolledText(w, width=70, height=24, font=TEXT_FONT, padx=15, pady=15)
    txt.insert("1.0", record)
    txt.config(state="disabled", bg="#FDFEFE", foreground=COLOR_SECONDARY_DARK, relief="flat", borderwidth=2)
    txt.pack(padx=20, pady=20)
    
    ttk.Button(w, text="Close Record", style="Success.TButton", command=w.destroy).pack(pady=(0, 15))
    center(w)

def open_doctor_login_window():
    win = tk.Toplevel(root)
    win.title("Doctor Login")
    win.configure(bg=COLOR_BACKGROUND_LIGHT)
    win.grab_set()

    header = tk.Frame(win, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="Doctor Login", bg=COLOR_HEADER_BG, fg="white", font=("Helvetica", 16, "bold"), pady=10).pack(fill="x", padx=10)

    frm = ttk.Frame(win, padding="20 20 20 20", relief="groove"); frm.pack(pady=20, padx=30)
    
    ttk.Label(frm, text="Doctor ID:", font=("Helvetica", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    id_ent = ttk.Entry(frm, width=25); id_ent.grid(row=0, column=1, padx=10, pady=10)
    
    ttk.Label(frm, text="Password:", font=("Helvetica", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    pw_ent = ttk.Entry(frm, show="*", width=25); pw_ent.grid(row=1, column=1, padx=10, pady=10)
    
    ttk.Button(win, text="Login (Password + OTP)", 
               style="Primary.TButton",
               command=lambda: doctor_login_with_otp(win, id_ent.get().strip(), pw_ent.get().strip())).pack(pady=(10, 20))
    
    center(win)

def open_patient_access_window(doc_id):
    w = tk.Toplevel(root)
    w.title(f"Doctor: {doc_id} - Patient Access")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)

    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text=f"Access Panel | Doctor: {doc_id}", bg=COLOR_HEADER_BG, fg="white", font=("Helvetica", 16, "bold"), pady=10).pack(fill="x", padx=10)
    
    # Primary Actions Group
    primary_frame = ttk.LabelFrame(w, text=" Patient Authentication ", padding="15 10 15 15")
    primary_frame.pack(pady=20, padx=30, fill="x")
    
    ttk.Button(primary_frame, text="Start Patient MFA (Face + OTP + Voice)", 
               style="Primary.TButton",
               command=lambda: patient_mfa_flow(doc_id)).pack(pady=10, padx=10, fill="x")
               
    ttk.Button(primary_frame, text="Emergency Override (Requires Primary Doc OTP)", 
               style="Accent.TButton",
               command=lambda: emergency_override_flow(doc_id)).pack(pady=10, padx=10, fill="x")

    # Security Actions Group
    security_frame = ttk.LabelFrame(w, text=" Security & Audit ", padding="15 10 15 15")
    security_frame.pack(pady=(0, 20), padx=30, fill="x")

    ttk.Button(security_frame, text="Run Anomaly Check (Audit Logs)", 
               style="Success.TButton",
               command=lambda: threading.Thread(target=run_anomaly_check_thread).start()).pack(pady=10, padx=10, fill="x")
               
    ttk.Button(w, text="Logout", 
               command=w.destroy).pack(pady=(0, 15))
    center(w)
    
def run_anomaly_check_thread():
    """Runs anomaly check in a separate thread and shows progress."""
    
    # Temporary loading window
    loading_win = tk.Toplevel(root)
    loading_win.title("Analysis Running")
    loading_win.config(bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20)
    loading_win.grab_set()
    tk.Label(loading_win, text="Analyzing login patterns...", bg=COLOR_BACKGROUND_LIGHT).pack(pady=10)
    
    # Progress Bar
    progress = ttk.Progressbar(loading_win, orient="horizontal", length=200, mode="indeterminate")
    progress.pack(pady=10)
    progress.start(15)
    center(loading_win)
    
    try:
        result = check_for_anomalies()
        progress.stop()
        loading_win.destroy()
        messagebox.showinfo("Anomaly Check Result", result)
    except Exception as e:
        progress.stop()
        loading_win.destroy()
        messagebox.showerror("Anomaly Check Error", f"An unexpected error occurred during analysis: {e}")


def setup_admin_panel(notebook):
    """Sets up the Records and Logs tabs within the Admin Panel Notebook."""
    
    # --- Tab 1: Records Summary ---
    records_tab = ttk.Frame(notebook, padding="10 10 10 10")
    notebook.add(records_tab, text="Records Summary")

    btn_frame = ttk.Frame(records_tab); btn_frame.pack(fill="x", pady=(0, 10))
    
    ttk.Button(btn_frame, text="Register Doctor", style="Success.TButton", command=register_doctor).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Register Patient", style="Success.TButton", command=register_patient).pack(side="left", padx=5)
    
    cols = ("Type", "ID", "Contact")
    tree = ttk.Treeview(records_tab, columns=cols, show="headings", height=18)
    for col in cols: tree.heading(col, text=col)
    tree.column("Type", width=120, anchor="center")
    tree.column("ID", width=220)
    tree.column("Contact", width=360)
    tree.pack(fill="both", expand=True)

    def load_records():
        tree.delete(*tree.get_children())
        doctors, patients = get_all_records_summary()
        if not doctors and not patients:
            tree.insert("", "end", values=("SYSTEM", "No Records Found", "DB Empty/Failed"))
        else:
            for d in doctors:
                tree.insert("", "end", values=("Doctor", d["id"], d["contact"]))
            for p in patients:
                tree.insert("", "end", values=("Patient", p["id"], p["contact"]))
    
    def delete_selected_gui():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select entries to delete.")
            return
        if not messagebox.askyesno ("Confirm Delete", "Delete selected records (cannot be undone)?"):
            return
            
        success_count = 0
        for iid in sel:
            vals = tree.item(iid, "values")
            typ, idv = vals[0], vals[1]
            if delete_record_db(typ, idv):
                success_count += 1
        
        load_records() # Refresh the view
        messagebox.showinfo("Deleted", f"{success_count} records deleted from DB.")
        
    load_records()
    
    ttk.Button(btn_frame, text="Delete Selected", style="Accent.TButton", command=delete_selected_gui).pack(side="right", padx=5)
    ttk.Button(btn_frame, text="Refresh", command=load_records).pack(side="right", padx=5)


    # --- Tab 2: Access Logs ---
    logs_tab = ttk.Frame(notebook, padding="10 10 10 10")
    notebook.add(logs_tab, text="Access Logs")
    
    # Use a Treeview for cleaner log display
    logs_cols = ("Time", "Doctor ID", "Patient ID", "Status", "Reason")
    logs_tree = ttk.Treeview(logs_tab, columns=logs_cols, show="headings")
    for col in logs_cols: logs_tree.heading(col, text=col)
    logs_tree.column("Time", width=150, anchor="center")
    logs_tree.column("Status", width=80, anchor="center")
    logs_tree.column("Doctor ID", width=100)
    logs_tree.column("Patient ID", width=100)
    logs_tree.column("Reason", width=250)
    logs_tree.pack(fill="both", expand=True, pady=(0, 10))

    def load_logs():
        logs_tree.delete(*logs_tree.get_children())
        logs = get_all_logs()
        for entry in logs:
            status = entry['status']
            tag = 'success' if status == 'SUCCESS' else 'fail'
            logs_tree.insert("", "end", values=(entry['time'], entry['doctor'], entry['patient'], status, entry['reason']), tags=(tag,))
        
        logs_tree.tag_configure('success', foreground=COLOR_ACCENT_SUCCESS, font=(TEXT_FONT.actual("family"), 9, 'bold'))
        logs_tree.tag_configure('fail', foreground=COLOR_ACCENT_DANGER, font=(TEXT_FONT.actual("family"), 9, 'bold'))

    load_logs()
    
    ttk.Button(logs_tab, text="Refresh Logs", style="Success.TButton", command=load_logs).pack(pady=5)


def open_admin_panel():
    w = tk.Toplevel(root)
    w.title("Admin Panel")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)
    w.grab_set()

    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="SmartMedID Admin Panel", bg=COLOR_HEADER_BG, fg="white", font=("Helvetica", 16, "bold"), pady=10).pack(fill="x", padx=10)
    
    # Tabbed Interface
    notebook = ttk.Notebook(w)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)
    
    setup_admin_panel(notebook)

    center(w)


# --- 8. MAIN DASHBOARD ---

if __name__ == "__main__":
    
    root = tk.Tk()
    TEXT_FONT = _fit_screen(root) 
    root.title("SmartMedID Secure Biometric System")
    
    # Use Grid for better centering
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    main_frame = tk.Frame(root, bg=COLOR_BACKGROUND_LIGHT)
    main_frame.grid(row=0, column=0, sticky="nsew")
    
    # Frame to hold content, centered within main_frame
    content_frame = tk.Frame(main_frame, bg="white", relief="raised", borderwidth=2)
    
    # Center the content_frame dynamically (still needed for Tkinter Frame placement)
    def place_content(event=None):
        main_w = main_frame.winfo_width()
        main_h = main_frame.winfo_height()
        frame_w = content_frame.winfo_reqwidth()
        frame_h = content_frame.winfo_reqheight()
        x = (main_w - frame_w) // 2
        y = (main_h - frame_h) // 2
        content_frame.place(x=x, y=y)

    main_frame.bind('<Configure>', place_content)
    
    # Design the content_frame
    
    # Main Header
    header = tk.Frame(content_frame, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="SmartMedID Secure Biometric System", bg=COLOR_HEADER_BG, fg="white", font=("Helvetica", 20, "bold"), pady=20).pack(padx=30)

    # Sub-header/Motto
    tk.Label(content_frame, text="Your ID. Your Health. Secured.", bg="white", fg=COLOR_SECONDARY_DARK, font=("Helvetica", 12, "italic")).pack(pady=(5, 30))

    # Main Buttons 
    ttk.Button(content_frame, text="Doctor Mode (Login)", 
               style="Primary.TButton",
               width=30, 
               command=open_doctor_login_window).pack(pady=15, padx=50)
               
    ttk.Button(content_frame, text="Admin Panel", 
               style="Primary.TButton",
               width=30, 
               command=open_admin_panel).pack(pady=15, padx=50)
               
    ttk.Button(content_frame, text="Exit Application", 
               style="Accent.TButton",
               width=30, 
               command=root.quit).pack(pady=(15, 30), padx=50)

    # Ensure the content frame is initially placed correctly
    content_frame.update_idletasks()
    place_content() 

    root.mainloop()
