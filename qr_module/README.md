# 🎟️ Secure Access & QR Module

### 📖 What is this Module?
This module serves as the **Security and Attendance Layer** for the EventPass system. Its primary purpose is to bridge the gap between the physical event venue and our digital database. By using QR codes, we automate the check-in process, replacing manual entry with a high-speed computer vision solution that ensures data integrity.

---

### 🛠️ Key Features
*   **Encapsulated Tokenization**: Instead of plain text, we generate unique tokens formatted as `EP-REG-{User_ID}-{Event_ID}`. This binds a ticket to a specific user and a specific event simultaneously.
*   **Anti-Fraud Logic**: The system leverages the `UNIQUE` constraint from our `REGISTRATION` table. This ensures that a QR code cannot be duplicated or reused once the `Attendance_Status` is updated.
*   **Real-Time Database Sync**: The module doesn't just scan; it executes an automated SQL `UPDATE` to mark participants as `Attended` and logs the precise `Scan_Time`.
*   **Self-Healing File System**: It includes automated directory management to ensure the `static/qr_codes/` path exists, preventing system crashes during generation.

---

### 📁 Components
| Component | Function |
| :--- | :--- |
| **`qr_handler.py`** | The "Engine." It contains the logic for generating QR images using the `qrcode` library and decoding them via `OpenCV`. |
| **`reg_101_50.png`** | A verified sample image that proves the encoder and decoder are perfectly synced with the database schema. |

---

### 🚀 Team Integration (How to use it)
This module is designed to be called by both the **Frontend** and **Backend** teams:

#### **For the Registration Flow (Person 1/2):**
When a user successfully registers, call `generate_registration_qr()`. This creates the physical ticket the user will show at the door.
```python
from qr_module.qr_handler import generate_registration_qr

# Automatically creates the PNG in the static folder
generate_registration_qr(user_id=101, event_id=50)
