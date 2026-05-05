from flask import Blueprint, request, jsonify, session

event_bp = Blueprint('events', __name__)

@event_bp.route('/create_event', methods=['POST'])
def create_event():
    # Only Organizers should be here
    if session.get('role') != 'organizer':
        return jsonify({"error": "Unauthorized"}), 403

    title = request.form.get('title')
    date = request.form.get('date')
    
    # LOGIC: Once Aparna is done, we add db.session.add() here
    print(f"Creating event: {title} on {date}")
    
    return jsonify({"message": "Event created successfully!"})