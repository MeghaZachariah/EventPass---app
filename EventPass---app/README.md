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

## 🔐 Database & QR Module (Aparna)
I have implemented the core relational database architecture and the secure QR-based attendance tracking system.

### 1. Data Architecture & Security Logic
- **ISA Relationship**: Designed a specialized schema using an inheritance model to differentiate between `PARTICIPANT` and `ORGANIZER` roles.
- **Integrity Control**: Enforced data consistency using `FOREIGN KEY` constraints and `ON DELETE CASCADE` triggers.
- **Attendance Workflow**: Developed a system where unique registration IDs are encrypted into QR codes and synced with the database upon scanning.

### 2. Project Structure

**Database Module**
- `database/schema.sql`: The SQL blueprint for all 6 tables and relational constraints.
- `database/db_setup.py`: Automation script to initialize the SQLite database file.

**QR Module**
- `qr_module/generate_qr.py`: Logic for creating and saving unique registration codes to `qr_images/`.
- `qr_module/scan_qr.py`: Attendance module using OpenCV to decode tickets and update database status.

### 3. How to Run
From the root folder, initialize the database:
`python database/db_setup.py`

Install dependencies for the QR module:
`pip install qrcode[pil] opencv-python`

## FRONTEND & OVERALL (KHADIJA SHIZA)
**Technical Overview**
EventPass is a full-stack application designed to automate the event registration process through dynamic QR code generation. The project demonstrates the integration of a Python backend with a responsive JavaScript frontend to handle real-time data processing and verification.

**Key Contributions & Implementation:**
Backend Engineering: Developed a RESTful API using Flask and SQLAlchemy to manage user authentication, event lifecycles, and registration records.

Database Design: Implemented a relational database schema in SQLite, applying normalization techniques (1NF to 3NF) to ensure data integrity and efficient querying.

Dynamic QR Module: Built a custom Python module using importlib and qrcode libraries to generate unique entry passes (e.g., qr_4_1.png) immediately upon successful registration.

Frontend Logic: Engineered a dynamic UI using JavaScript (ES6+) and the Fetch API to handle asynchronous requests, allowing for seamless state updates and pass retrieval without page reloads.

File Handling & Routing: Configured custom Flask routes to securely serve static assets and dynamically generated media from protected directories.

**Tech Stack:**
Backend: Python 3.x, Flask, SQLAlchemy

Frontend: JavaScript, HTML5, CSS3

Database: SQLite

Version Control: Git/GitHub