import os
import sys
import importlib.util
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
qr_path = os.path.join(project_root, "qr_module", "generate_qr.py")
try:
    spec = importlib.util.spec_from_file_location("generate_qr", qr_path)
    qr_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qr_module)
    
    generate_registration_qr = qr_module.generate_registration_qr
    print("[SUCCESS] QR Module loaded via direct path!")
except Exception as e:
    print(f"[ERROR] QR Module failed: {e}")
    def generate_registration_qr(u_id, e_id):
        print(f"Fallback: Registration QR for User {u_id}, Event {e_id}")
from extensions import db
from models import User, Event, Registration
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS 
from dotenv import load_dotenv
from datetime import datetime # Added for registration timestamps
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
CORS(app) 

# Configuration
app.secret_key = "my_temporary_secret_key_123"
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "..", "database", "eventpass.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app) 

with app.app_context():
    db.create_all()

# --- AUTH ROUTES ---

from flask import send_from_directory

# This route serves the actual login page
@app.route('/')
def index():
    # Adjust '../frontend' if your frontend folder is in a different spot relative to app.py
    return send_from_directory('../frontend', 'login.html')

# This route serves other static files (CSS, JS, images)
@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('../frontend', path)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
        
    username = data.get('name') 
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'participant').lower() # Get the role from frontend

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    try:
        new_user = User(name=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # If they chose 'organizer', add them to the ORGANIZER table
        if role == 'organizer':
            db.session.execute(
                db.text("INSERT INTO ORGANIZER (User_ID) VALUES (:uid)"),
                {"uid": new_user.user_id}
            )
            db.session.commit()

        return jsonify({"message": "Signup successful!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()
    
    if user:
        session['user_id'] = user.user_id
        session['username'] = user.name
        
        role = 'participant'
        try:
            # Checking role via text-based query since we are in a CS engineering project
            is_organizer = db.session.execute(
                db.text("SELECT 1 FROM ORGANIZER WHERE User_ID = :uid"),
                {"uid": user.user_id}
            ).fetchone()
            if is_organizer:
                role = 'organizer'
        except Exception:
            role = 'participant'

        session['role'] = role

        return jsonify({
            "message": "Login successful",
            "username": user.name,
            "user_id": user.user_id,
            "role": role
        }), 200
    
    # This was outside the if/else block in your version, which would cause an error
    return jsonify({"error": "Invalid Credentials"}), 401

# Renamed to avoid conflict with the /dashboard folder
@app.route('/dashboard_view')
def dashboard_view():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    template = 'organizer.html' if session.get('role') == 'organizer' else 'dashboard.html'
    return render_template(template, name=session.get('username'))
@app.route('/get_events', methods=['GET'])
def get_events():
    try:
        events = Event.query.all()
        event_list = []
        for event in events:
            event_list.append({
                "id": event.event_id,
                "title": event.title,
                "date": event.date,
                "location": event.location,
                "capacity": event.capacity
            })
        return jsonify(event_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/register_event', methods=['POST'])
def register_event():
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    if not user_id or not event_id:
        return jsonify({"error": "Missing user_id or event_id"}), 400

    # 1. Check if user is already registered to avoid duplicates
    existing_reg = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_reg:
        return jsonify({"message": "Already registered", "user_id": user_id, "event_id": event_id}), 200

    # 2. CREATE the registration in the database
    new_reg = Registration(
        user_id=user_id,
        event_id=event_id,
        reg_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        attendance_status="Absent"
    )
    
    try:
        db.session.add(new_reg)
        db.session.commit()
        
        # 3. GENERATE the QR code (This is why it wasn't working before!)
        # This calls your imported generate_registration_qr function
        generate_registration_qr(user_id, event_id)
        
        return jsonify({
            "message": "Registration successful!",
            "user_id": user_id,
            "event_id": event_id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Registration Error: {e}")
        return jsonify({"error": "Failed to complete registration: " + str(e)}), 500
from flask import send_from_directory
@app.route('/qr_module/qr_images/<path:filename>')
def custom_static(filename):
    qr_folder_path = os.path.join(os.path.dirname(basedir), 'qr_module', 'qr_images')
    return send_from_directory(qr_folder_path, filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)