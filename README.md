# EventPass
EventPass is a mobile-first web app streamlining event management. Organizers can create events and scan QR codes for real-time attendance tracking. Participants can browse, register, and receive unique entry codes. Built with a responsive design and secure role-based access, it simplifies the entire lifecycle of event organization.

## 🛠️ Backend Setup (Megha)
I've refactored the app to fix circular imports and sync with the database schema.

### 1. Environment Variables
Create a `.env` file in the root directory and add:
`FLASK_SECRET=your_generated_hex_key`

### 2. Project Structure
- `backend/app.py`: Main entry point (Run this!)
- `backend/models.py`: Database tables (User, Event, Registration)
- `backend/extensions.py`: Shared SQLAlchemy instance
- `backend/routes/`: Blueprint-based routes

### 3. How to Run
From the root folder:
`python backend/app.py`