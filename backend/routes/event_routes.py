from flask import Blueprint, request, jsonify, session
from extensions import db
from models import Event

event_bp = Blueprint('events', __name__)

@event_bp.route('/create_event', methods=['POST'])
def create_event():
    # Only Organizers should be able to create events
    if session.get('role') != 'organizer':
        return jsonify({"error": "Unauthorized"}), 403

    # Create new event object using form data from the frontend
    new_event = Event(
        title=request.form.get('title'),
        date=request.form.get('date'),
        location=request.form.get('location'),
        capacity=request.form.get('capacity'),
        organizer_id=session.get('user_id')
    )

    db.session.add(new_event)
    db.session.commit()
    
    return jsonify({"message": "Event created successfully!", "event_id": new_event.event_id})

@event_bp.route('/get_events', methods=['GET'])
def get_events():
    # Fetch all events from the database
    events = Event.query.all()
    
    # Convert database objects into a list of dictionaries (JSON)
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