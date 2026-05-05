from flask import Blueprint, request, jsonify, session

reg_bp = Blueprint('registration', __name__)

@reg_bp.route('/register_event', methods=['POST'])
def register_event():
    # 1. Check if user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401

    # 2. Get the event ID from Shiza's frontend
    event_id = request.form.get('event_id')
    user_id = session.get('user_id')

    # 3. MOCK LOGIC (Until Aparna finishes the REGISTRATION table)
    # This is where we will eventually check if the user is already registered
    print(f"User {user_id} is requesting to join Event {event_id}")

    # 4. Trigger for Aparna's QR Module
    # Once registration is confirmed, we'll call: generate_qr(user_id, event_id)
    
    return jsonify({
        "message": "Registration successful!",
        "event_id": event_id,
        "status": "pending_qr"
    })