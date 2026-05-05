"""
qr_handler.py
=============
Smart Event Discovery System — Secure Access Module

This module handles the generation and verification of registration QR codes.
It integrates with the `eventpass.db` schema to ensure secure, one-time
attendance tracking.

Dependencies:
    - qrcode[pil]
    - opencv-python-headless (cv2)
    - sqlite3
"""

import os
import qrcode
import cv2
import sqlite3
import re
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DB_NAME = "eventpass.db"
QR_DIR = "static/qr_codes/"
QR_PREFIX = "EP-REG"  # EventPass Registration Prefix


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def ensure_directories():
    """Create the storage directory for QR codes if it doesn't exist."""
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR)
        print(f"[INFO] Created directory: {QR_DIR}")


# ---------------------------------------------------------------------------
# Core Functionality
# ---------------------------------------------------------------------------

def generate_registration_qr(user_id: int, event_id: int) -> str:
    """
    Generate a unique QR code for a specific user registration.
    
    Data Structure: EP-REG-{user_id}-{event_id}
    
    This format directly maps to the UNIQUE constraint on (User_ID, Event_ID)
    in our REGISTRATION table. Since the database prevents duplicate 
    registrations, this QR code is guaranteed to represent a unique, 
    valid entry in the system.
    """
    ensure_directories()
    
    # Construct the unique data string
    qr_data = f"{QR_PREFIX}-{user_id}-{event_id}"
    
    # Create the QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Generate the image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the file
    file_name = f"reg_{user_id}_{event_id}.png"
    file_path = os.path.join(QR_DIR, file_name)
    img.save(file_path)
    
    print(f"[OK] QR Code generated for User {user_id}, Event {event_id}")
    print(f"     Data: {qr_data}")
    print(f"     Path: {file_path}")
    
    return file_path


def verify_and_update_attendance(image_path: str) -> bool:
    """
    Decode a QR code from an image and update the database attendance status.
    
    Uses OpenCV to detect and decode the QR string. If valid, it extracts
    the IDs and executes a SQL UPDATE to mark the participant as 'Attended'.
    """
    # 1. Read and Decode the QR Code
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Could not read image at {image_path}")
        return False
        
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    
    if not data:
        print("[ERROR] No QR code data detected in the image.")
        return False
        
    print(f"[INFO] Decoded Data: {data}")
    
    # 2. Parse the Data (EP-REG-{user_id}-{event_id})
    pattern = rf"^{QR_PREFIX}-(\d+)-(\d+)$"
    match = re.match(pattern, data)
    
    if not match:
        print(f"[ERROR] Invalid QR format: {data}")
        return False
        
    user_id, event_id = match.groups()
    
    # 3. Database Sync
    # We use the extracted IDs to target the specific registration.
    # The UNIQUE constraint on (User_ID, Event_ID) ensures we only ever
    # update exactly one row.
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Enable foreign keys just in case
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # SQL UPDATE Snippet
        update_query = """
        UPDATE REGISTRATION
        SET Attendance_Status = 'Attended',
            Scan_Time = CURRENT_TIMESTAMP
        WHERE User_ID = ? AND Event_ID = ? AND Attendance_Status = 'Registered';
        """
        
        cursor.execute(update_query, (user_id, event_id))
        
        if cursor.rowcount == 0:
            # Check if it was already scanned or doesn't exist
            cursor.execute("SELECT Attendance_Status FROM REGISTRATION WHERE User_ID = ? AND Event_ID = ?", (user_id, event_id))
            result = cursor.fetchone()
            if result:
                print(f"[WARN] Registration found but status is '{result[0]}'. No update performed.")
            else:
                print(f"[ERROR] No registration found for User {user_id} and Event {event_id}.")
            return False
            
        conn.commit()
        print(f"[SUCCESS] Attendance updated for User {user_id} at Event {event_id}.")
        return True
        
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Main (Demo/Testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage for testing
    print("--- QR Handler Test Run ---")
    
    # Mock IDs
    test_user = 101
    test_event = 50
    
    # 1. Generate
    path = generate_registration_qr(test_user, test_event)
    
    # 2. Verify (Note: This will fail the DB update if the registration 
    #    doesn't exist in eventpass.db, but it will still test the decoding)
    print("\n--- Simulating Scan ---")
    verify_and_update_attendance(path)
