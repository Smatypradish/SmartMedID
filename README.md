# SmartMedID: Secure Face Biometrics-Based Medical Record Access System

## Overview
SmartMedID is a privacy-focused healthcare solution built using Python. It enables secure, seamless access to encrypted electronic medical records using face biometrics, OTP, and voice verification. Doctor credentials are protected using SHA-256, and all access is fully logged for accountability.

## Features
- Face recognition for patient authentication
- Fernet-encrypted patient records
- SHA-256 hashed doctor credentials
- OTP and voice-based multi-factor authentication
- Admin and audit logging
- Tkinter GUI

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your PostgreSQL database (see `db_utils.py`).
3. Update email and DB credentials in code or via environment variables.
4. Run the dashboard:
   ```bash
   python smartmedid_dashboard.py
   ```

## Project Report

See `SmartMedID_Report.md` for the full academic report.

## Authors

- Mano.K, Dhayanidhi J P, Pradish G  
  School of Computer Science Engineering and Information Systems,  
  Vellore Institute of Technology, Vellore, Tamilnadu, India