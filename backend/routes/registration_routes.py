from flask import Blueprint, request, jsonify, session
from extensions import db
from models import Registration, Event
from datetime import datetime

reg_bp = Blueprint('registration', __name__)

@reg_bp.route('/register_event', methods=['POST'])
def register_event():
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401

    event_id = request.form.get('event_id')
    user_id = session.get('user_id')

    # Check if already registered
    existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({"message": "Already registered for this event"}), 400

    new_reg = Registration(
        user_id=user_id,
        event_id=event_id,
        reg_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        attendance_status="Absent"
    )

    db.session.add(new_reg)
    db.session.commit()
    
    return jsonify({"message": "Registration successful!"})