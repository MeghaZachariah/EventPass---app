# Database Module
This folder contains the SQLite database and the setup script for the EventPass system.

## Files
* `create_eventpass_db.py`: The Python script that generates the database schema.
* `eventpass.db`: The actual SQLite database file.

## Features Implemented
* **Duplicate Detection**: Uses a `UNIQUE` constraint on User_ID and Event_ID in the Registration table[cite: 1].
* **ISA Subtyping**: Implements specific roles for Participants and Organizers[cite: 1].
* **Integrity**: Enforces foreign key constraints and capacity limits[cite: 1].
