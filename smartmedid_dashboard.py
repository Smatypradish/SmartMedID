import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import os, random, smtplib, time, sys
from email.mime.text import MIMEText
from datetime import datetime
import tkinter.font as tkfont
import csv
import threading 

# --- ESSENTIAL LIBRARY IMPORTS ---
try:
    from PIL import Image, ImageTk 
except ImportError:
    class DummyImage:
        @staticmethod
        def open(path): return DummyImage()
        def resize(self, w, h, resample): return self
    Image = DummyImage
    ImageTk = DummyImage


# Import all core logic functions
from smartmedid_logic import (
    hash_password, log_access, enroll_doctor_db, get_doctor_auth_data,
    enroll_patient_db, get_patient_data_for_mfa, decrypt_patient_record,
    get_patient_email, get_patient_record_by_id, get_all_records_summary,
    delete_record_db, get_all_logs,
    check_for_anomalies # Anomaly Check still available
)

# Initialize OpenCV, Face Recognition, and Speech Recognition
try:
    import cv2, face_recognition
except ImportError:
    cv2 = None
    face_recognition = None
try:
    import speech_recognition as sr
except ImportError:
    sr = None

# --- 1. CONFIGURATION (CRITICAL) ---
GMAIL_SENDER = "smatypradish@gmail.com" 
GMAIL_APP_PASS = "ygha pjwm vebm bqnj" # <-- UPDATE YOUR GMAIL APP PASSWORD
MICROPHONE_INDEX = None 
OTP_EXPIRY_SECONDS = 60
OTP_STORE = {} 
TEXT_FONT = None 
BACKGROUND_IMAGE = None 

# --- 2. THEME DEFINITION ---
COLOR_PRIMARY_BLUE = "#007BFF"  
COLOR_SECONDARY_DARK = "#343A40"  
COLOR_BACKGROUND_LIGHT = "#F8F9FA" 
COLOR_HEADER_BG = "#0056B3"       
COLOR_ACCENT_SUCCESS = "#28A745" 
COLOR_ACCENT_DANGER = "#DC3545"  

# --- 3. WINDOW HELPERS ---

def _fit_screen(root):
    """Sets initial window size and configures fonts and ttk styles."""
    
    root.state("zoomed")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    def_font = tkfont.nametofont("TkDefaultFont")
    def_font.config(size=max(9, int(h/96)))

    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("TLabel", background=COLOR_BACKGROUND_LIGHT, foreground=COLOR_SECONDARY_DARK)
    style.configure("TFrame", background=COLOR_BACKGROUND_LIGHT)

    style.configure("Treeview", rowheight=max(25,int(h/45)), font=def_font, background="white", foreground=COLOR_SECONDARY_DARK, fieldbackground="white")
    style.map("Treeview", background=[('selected', COLOR_PRIMARY_BLUE)])

    style.configure("Treeview.Heading", font=(def_font.actual("family"), max(10,int(h/90)), "bold"), background=COLOR_PRIMARY_BLUE, foreground="white")

    style.configure("Primary.TButton", padding=(15, 8), font=("Arial", 10, "bold"), background=COLOR_PRIMARY_BLUE, foreground="white")
    style.map("Primary.TButton", background=[("active", "#0056B3"), ("pressed", "#004080")], foreground=[("active", "white")])
               
    style.configure("Accent.TButton", padding=(15, 8), font=("Arial", 10, "bold"), background=COLOR_ACCENT_DANGER, foreground="white")
    style.map("Accent.TButton", background=[("active", "#B31F2A"), ("pressed", "#8F0E18")])


    return tkfont.Font(family="Courier", size=max(9, int(h/110)))

def center(win):
    """Centers a window on the screen."""
    win.update_idletasks()
    w = win.winfo_width(); h = win.winfo_height()
    sw = win.winfo_screenwidth(); sh = win.winfo_screenheight()
    x = (sw - w) // 2; y = (sh - h) // 2
    win.geometry(f"+{x}+{y}")

# --- 4. CAMERA & FACE LOGIC (Simplified) ---

def capture_face(title, prompt):
    if cv2 is None or face_recognition is None:
        messagebox.showerror("Dependency", "OpenCV and face_recognition required.")
        return None
    
    # Try index 0 first, as it is the standard
    cap = cv2.VideoCapture(0) 
    
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot open camera. Try closing all other video apps.")
        return None

    messagebox.showinfo(title, prompt)
    captured_encoding = None

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # --- CRITICAL POINT ---
        # The app might be crashing here due to dependency issues.
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

    # Try index 0 first, as it is the standard
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): 
        messagebox.showerror("Camera Error", "Cannot open camera. Try closing all other video apps.")
        return None

    # Liveness check is REMOVED, proceeding directly to face probe.
    
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
    
def patient_voice_verify(prompt_phrase="my health is my id", timeout=5):
    # (Voice verification logic remains the same)
    if sr is None:
        messagebox.showerror("Dependency", "Speech recognition required.")
        return False
        
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
            messagebox.showinfo("Voice Verification", f"Say: '{prompt_phrase}'")
            r.adjust_for_ambient_noise(source, duration=0.7)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=timeout)
            text = r.recognize_google(audio)
            
            return prompt_phrase.lower() in text.lower()
            
    except Exception as e:
        messagebox.showerror("Voice Error", f"Voice verification failed: {e}")
        return False
        
# --- 5. CORE APPLICATION FLOWS (Doctor Face Removed) ---

def register_doctor():
    doc_id = simpledialog.askstring("Register Doctor", "Enter Doctor ID:")
    if not doc_id: return
    
    pwd = simpledialog.askstring("Register Doctor", "Enter password:", show="*")
    email = simpledialog.askstring("Register Doctor", "Enter doctor email (for OTP):")
    if not pwd or not email: return
    
    face_encoding = None 
    
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
            
    tk.Label(otp_win, text=f"OTP sent to: {email}").pack(pady=6)
    code_ent = tk.Entry(otp_win); code_ent.pack(pady=6)
    tk.Button(otp_win, text="Submit", command=submit_otp).pack(pady=6)
    center(otp_win)


def patient_mfa_flow(doctor_id):
    # 1. Face Probe (No Liveness Check)
    pid = authenticate_face_probe()
    if not pid:
        log_access(doctor_id, "Unknown", "FAIL", "Patient face not recognized")
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
        messagebox.showerror("Auth", "Voice verification failed.")
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

# --- 6. GUI WINDOWS ---

def show_decrypted_record(pid, record):
    w = tk.Toplevel(root)
    w.title(f"Patient Record: {pid}")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)
    
    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text=f"Patient Record: {pid}", bg=COLOR_HEADER_BG, fg="white", font=("Arial", 14, "bold"), pady=8).pack(fill="x", padx=10)
    
    txt = scrolledtext.ScrolledText(w, width=70, height=24, font=TEXT_FONT)
    txt.insert("1.0", record)
    txt.config(state="disabled", bg="#f0f8ff", foreground=COLOR_SECONDARY_DARK)
    txt.pack(padx=10, pady=10)
    
    center(w)

def open_doctor_login_window():
    win = tk.Toplevel(root)
    win.title("Doctor Login")
    win.configure(bg=COLOR_BACKGROUND_LIGHT)

    header = tk.Frame(win, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="Doctor Login", bg=COLOR_HEADER_BG, fg="white", font=("Arial", 14, "bold"), pady=8).pack(fill="x", padx=10)

    frm = ttk.Frame(win); frm.pack(pady=15, padx=20)
    
    ttk.Label(frm, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    id_ent = ttk.Entry(frm); id_ent.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frm, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    pw_ent = ttk.Entry(frm, show="*"); pw_ent.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Button(win, text="Login (Pass + OTP)", 
               style="Primary.TButton",
               command=lambda: doctor_login_with_otp(win, id_ent.get().strip(), pw_ent.get().strip())).pack(pady=15)
    
    center(win)

def open_patient_access_window(doc_id):
    w = tk.Toplevel(root)
    w.title(f"Doctor: {doc_id} - Patient Access")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)

    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text=f"Access Panel | Doctor: {doc_id}", bg=COLOR_HEADER_BG, fg="white", font=("Arial", 14, "bold"), pady=8).pack(fill="x", padx=10)
    
    ttk.Button(w, text="Start Patient MFA (Face + OTP + Voice)", 
               style="Primary.TButton",
               command=lambda: patient_mfa_flow(doc_id)).pack(pady=15, padx=20)
               
    ttk.Button(w, text="Emergency Override", 
               style="Accent.TButton",
               command=lambda: emergency_override_flow(doc_id)).pack(pady=5, padx=20)
               
    ttk.Button(w, text="Run Anomaly Check", 
               style="Primary.TButton",
               command=lambda: threading.Thread(target=run_anomaly_check_thread).start()).pack(pady=5, padx=20)
               
    ttk.Button(w, text="Close", 
               command=w.destroy).pack(pady=15)
    center(w)
    
def run_anomaly_check_thread():
    """Runs anomaly check in a separate thread to prevent GUI freeze."""
    messagebox.showinfo("Anomaly Check", "Starting Anomaly Detection on log data. This may take a moment.")
    result = check_for_anomalies()
    messagebox.showinfo("Anomaly Check Result", result)


def open_admin_panel():
    w = tk.Toplevel(root)
    w.title("Admin Panel")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)

    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="SmartMedID Admin Panel", bg=COLOR_HEADER_BG, fg="white", font=("Arial", 14, "bold"), pady=8).pack(fill="x", padx=10)
    
    btn_frame = ttk.Frame(w); btn_frame.pack(fill="x", pady=8, padx=10)
    
    ttk.Button(btn_frame, text="Register Doctor", style="Primary.TButton", command=register_doctor).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Register Patient", style="Primary.TButton", command=register_patient).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="View Logs", style="Primary.TButton", command=open_logs_card_view).pack(side="left", padx=5)
    
    cols = ("Type", "ID", "Contact")
    tree = ttk.Treeview(w, columns=cols, show="headings", height=18)
    for col in cols: tree.heading(col, text=col)
    tree.column("Type", width=120, anchor="center")
    tree.column("ID", width=220)
    tree.column("Contact", width=360)
    tree.pack(padx=12, pady=6, fill="both", expand=True)

    doctors, patients = get_all_records_summary()
    
    if not doctors and not patients:
        tree.insert("", "end", values=("SYSTEM", "No Records Found", "Database is empty or connection failed."))
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
                tree.delete(iid)
                success_count += 1
        
        messagebox.showinfo("Deleted", f"{success_count} records deleted from DB.")
        
    ttk.Button(btn_frame, text="Delete Selected", style="Accent.TButton", command=delete_selected_gui).pack(side="right", padx=5)
    center(w)
    
def open_logs_card_view():
    w = tk.Toplevel(root)
    w.title("Access Logs (Cards)")
    w.configure(bg=COLOR_BACKGROUND_LIGHT)

    header = tk.Frame(w, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="Access Logs Audit Trail", bg=COLOR_HEADER_BG, fg="white", font=("Arial", 14, "bold"), pady=8).pack(fill="x", padx=10)

    logs = get_all_logs()

    canvas = tk.Canvas(w, bg=COLOR_BACKGROUND_LIGHT); canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(w, orient="vertical", command=canvas.yview); scrollbar.pack(side="right", fill="y")
    container = ttk.Frame(canvas); container.config(padding=(10, 10))
    canvas.create_window((0,0), window=container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    if not logs:
        ttk.Label(container, text="No logs yet.", font=("Arial", 10, "italic")).pack(pady=10)
        return
        
    for entry in logs:
        frame = ttk.Frame(container, relief="flat", padding=10)
        frame.config(style="TFrame")
        frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(frame, text=f"Time: {entry['time']}", bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_PRIMARY_BLUE, font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(frame, text=f"Doctor: {entry['doctor']} | Patient: {entry['patient']}", bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_SECONDARY_DARK).pack(anchor="w")
        
        status_color = COLOR_ACCENT_SUCCESS if entry['status'] == 'SUCCESS' else COLOR_ACCENT_DANGER
        tk.Label(frame, text=f"Status: {entry['status']} | Reason: {entry['reason']}", bg=COLOR_BACKGROUND_LIGHT, fg=status_color, font=("Arial", 9, "bold")).pack(anchor="w", pady=(2, 0))
        
    container.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    center(w)


# --- 8. MAIN DASHBOARD ---

if __name__ == "__main__":
    
    root = tk.Tk()
    # Call _fit_screen first to initialize styling and global variables
    TEXT_FONT = _fit_screen(root) 
    root.title("SmartMedID Dashboard")
    
    # We use a simple frame as the main container
    main_frame = tk.Frame(root, bg=COLOR_BACKGROUND_LIGHT)
    main_frame.pack(fill="both", expand=True)
    
    # Create a frame to hold the content, placed in the center
    content_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND_LIGHT)
    
    # Center the content_frame inside the main window
    def place_content(event=None):
        main_w = main_frame.winfo_width()
        main_h = main_frame.winfo_height()
        frame_w = content_frame.winfo_reqwidth()
        frame_h = content_frame.winfo_reqheight()
        
        x = (main_w - frame_w) // 2
        y = (main_h - frame_h) // 2
        
        content_frame.place(x=x, y=y)

    main_frame.bind('<Configure>', place_content)
    
    # Design the content_frame (The visible part of the dashboard)
    
    # Main Header
    header = tk.Frame(content_frame, bg=COLOR_HEADER_BG)
    header.pack(fill="x")
    tk.Label(header, text="SmartMedID Secure Biometric System", bg=COLOR_HEADER_BG, fg="white", font=("Arial", 18, "bold"), pady=15).pack(padx=12)

    # Main Buttons 
    ttk.Button(content_frame, text="Doctor Mode (Login)", 
               style="Primary.TButton",
               width=30, 
               command=open_doctor_login_window).pack(pady=(30, 10))
               
    ttk.Button(content_frame, text="Admin Panel", 
               style="Primary.TButton",
               width=30, 
               command=open_admin_panel).pack(pady=8)
               
    ttk.Button(content_frame, text="Exit", 
               style="Accent.TButton",
               width=30, 
               command=root.quit).pack(pady=15)

    # Ensure the content frame is initially placed correctly
    content_frame.update_idletasks()
    place_content() 

    root.mainloop()
