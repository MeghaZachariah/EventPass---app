# EventPass
EventPass is a mobile-first web app streamlining event management. Organizers can create events and scan QR codes for real-time attendance tracking. Participants can browse, register, and receive unique entry codes. Built with a responsive design and secure role-based access, it simplifies the entire lifecycle of event organization.

🚀 EventPass – Backend API Specification (Phase 1)
This document outlines the endpoints and data requirements for the EventPass system.

🛠 Tech Stack
Backend: Flask

Database: SQLite

Frontend: HTML/CSS/JS

📡 API Endpoints for Frontend 
Shiza, please ensure your <form> tags and fetch() calls match these exactly. Use POST for all data submissions.

Shiza, please use these endpoints for your forms and fetch() calls. All data submissions should use the POST method.

1. User Signup

Endpoint: /signup

Method: POST

Required Form Names: username, email, password, role

2. User Login

Endpoint: /login

Method: POST

Required Form Names: email, password

3. Create Event

Endpoint: /create_event

Method: POST

Required Form Names: title, description, date, location

4. Register for Event

Endpoint: /register_event

Method: POST

Required Form Names: event_id

🗄 Database Requirements (Person 3)
Aparna, the backend logic is being built around these table expectations:

USER Table: Stores unique id, username, email, hashed password, and the role (Participant or Organizer).

EVENT Table: Stores event details and must include a foreign key linking to the ORGANIZER.

REGISTRATION Table: This is the many-to-many link between PARTICIPANT and EVENT.

QR_PASS Table: A weak entity linked to the PARTICIPANT.

🏃 How to Run the Backend
Navigate to the backend/ folder.

Activate the virtual environment using .venv\Scripts\activate.

Install dependencies via pip install -r requirements.txt.

Run the server using python app.py.