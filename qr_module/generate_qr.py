import qrcode
import os

# Configuration
QR_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "qr_images")

def ensure_dir():
    """Ensure the qr_images directory exists."""
    if not os.path.exists(QR_IMAGE_DIR):
        os.makedirs(QR_IMAGE_DIR)
        print(f"[INFO] Created directory: {QR_IMAGE_DIR}")

def generate_registration_qr(user_id, event_id):
    """
    Generates a QR code for a specific registration.
    
    Data: EP-REG-{user_id}-{event_id}
    Saves to: qr_module/qr_images/
    Returns: Absolute file path
    """
    ensure_dir()
    
    # 1. Create the unique data string
    qr_data = f"EP-REG-{user_id}-{event_id}"
    
    # 2. Generate the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 3. Save the image
    file_name = f"qr_{user_id}_{event_id}.png"
    file_path = os.path.join(QR_IMAGE_DIR, file_name)
    img.save(file_path)
    
    print(f"[OK] QR Code generated: {file_path}")
    return file_path

if __name__ == "__main__":
    # Test generation
    generate_registration_qr(1, 101)
