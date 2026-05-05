"""
create_eventpass_db.py
======================
Smart Event Discovery System — Database Initialisation Script

Creates the SQLite database `eventpass.db` with the following schema:

    USER          — Core identity table for every account holder.
    PARTICIPANT   — Subtype of USER for attendees (ISA relationship).
    ORGANIZER     — Subtype of USER for event organisers (ISA relationship).
    EVENT         — Events created and owned by an ORGANIZER.
    REGISTRATION  — Junction table linking PARTICIPANTs to EVENTs, with a
                    UNIQUE constraint on (User_ID, Event_ID) to prevent
                    duplicate registrations.

Foreign-key enforcement is enabled explicitly via PRAGMA foreign_keys = ON.
"""

import sqlite3
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DB_NAME = "eventpass.db"


# ---------------------------------------------------------------------------
# DDL Statements
# ---------------------------------------------------------------------------

# USER — base identity table shared by both PARTICIPANTs and ORGANIZERs.
# Email is declared UNIQUE so that no two accounts can share the same address.
CREATE_USER = """
CREATE TABLE IF NOT EXISTS USER (
    User_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
    Name     TEXT    NOT NULL,
    Email    TEXT    NOT NULL UNIQUE,
    Password TEXT    NOT NULL
);
"""

# PARTICIPANT — represents an attendee.
# User_ID is both the PRIMARY KEY and a FOREIGN KEY referencing USER,
# implementing a one-to-one ISA (subtype) relationship.
CREATE_PARTICIPANT = """
CREATE TABLE IF NOT EXISTS PARTICIPANT (
    User_ID INTEGER PRIMARY KEY,
    FOREIGN KEY (User_ID)
        REFERENCES USER (User_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

# ORGANIZER — represents an event organiser.
# Carries the additional Company_Name attribute beyond the base USER fields.
CREATE_ORGANIZER = """
CREATE TABLE IF NOT EXISTS ORGANIZER (
    User_ID      INTEGER PRIMARY KEY,
    Company_Name TEXT    NOT NULL,
    FOREIGN KEY (User_ID)
        REFERENCES USER (User_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

# EVENT — an event owned by exactly one ORGANIZER.
# Capacity must be a positive integer; Date is stored as TEXT in ISO-8601
# format (YYYY-MM-DD HH:MM:SS) for maximum SQLite compatibility.
CREATE_EVENT = """
CREATE TABLE IF NOT EXISTS EVENT (
    Event_ID     INTEGER PRIMARY KEY AUTOINCREMENT,
    Title        TEXT    NOT NULL,
    Date         TEXT    NOT NULL,
    Location     TEXT    NOT NULL,
    Capacity     INTEGER NOT NULL CHECK (Capacity > 0),
    Organizer_ID INTEGER NOT NULL,
    FOREIGN KEY (Organizer_ID)
        REFERENCES ORGANIZER (User_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

# REGISTRATION — links a PARTICIPANT to an EVENT.
# Reg_Date defaults to the current timestamp.
# Attendance_Status uses a CHECK constraint to enforce a controlled vocabulary.
# The UNIQUE constraint on (User_ID, Event_ID) prevents duplicate registrations.
CREATE_REGISTRATION = """
CREATE TABLE IF NOT EXISTS REGISTRATION (
    Reg_ID            INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID           INTEGER NOT NULL,
    Event_ID          INTEGER NOT NULL,
    Reg_Date          TEXT    NOT NULL DEFAULT (datetime('now')),
    Attendance_Status TEXT    NOT NULL DEFAULT 'Registered'
                              CHECK (Attendance_Status IN
                                     ('Registered', 'Attended', 'Absent', 'Cancelled')),
    Scan_Time         TEXT,
    FOREIGN KEY (User_ID)
        REFERENCES PARTICIPANT (User_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Event_ID)
        REFERENCES EVENT (Event_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    UNIQUE (User_ID, Event_ID)
);
"""

# Ordered list of (table_name, DDL) pairs — creation order respects FK deps.
TABLES = [
    ("USER",         CREATE_USER),
    ("PARTICIPANT",  CREATE_PARTICIPANT),
    ("ORGANIZER",    CREATE_ORGANIZER),
    ("EVENT",        CREATE_EVENT),
    ("REGISTRATION", CREATE_REGISTRATION),
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def get_table_info(cursor: sqlite3.Cursor, table_name: str) -> list[tuple]:
    """Return column metadata for *table_name* via PRAGMA table_info."""
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()


def get_foreign_keys(cursor: sqlite3.Cursor, table_name: str) -> list[tuple]:
    """Return foreign-key metadata for *table_name* via PRAGMA foreign_key_list."""
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    return cursor.fetchall()


def print_schema_summary(cursor: sqlite3.Cursor) -> None:
    """Print a human-readable summary of every table's columns and FK links."""
    print("\n" + "=" * 60)
    print("  DATABASE SCHEMA SUMMARY")
    print("=" * 60)

    for table_name, _ in TABLES:
        print(f"\n  TABLE: {table_name}")
        print("  " + "-" * 40)

        # Column details
        columns = get_table_info(cursor, table_name)
        print(f"  {'CID':<5} {'Column':<22} {'Type':<12} {'NotNull':<9} {'PK'}")
        print("  " + "-" * 58)
        for col in columns:
            cid, name, col_type, not_null, default, pk = col
            print(f"  {cid:<5} {name:<22} {col_type:<12} {str(bool(not_null)):<9} {bool(pk)}")

        # Foreign key details
        fks = get_foreign_keys(cursor, table_name)
        if fks:
            print(f"\n  Foreign Keys:")
            for fk in fks:
                _, seq, ref_table, from_col, to_col, on_update, on_delete, _ = fk
                print(f"    {from_col} -> {ref_table}.{to_col} "
                      f"[ON UPDATE {on_update}, ON DELETE {on_delete}]")

    print("\n" + "=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Main routine
# ---------------------------------------------------------------------------

def create_database(db_path: str = DB_NAME) -> None:
    """Create *db_path*, define all tables, and print a schema summary."""

    # Remove a stale database file so the script is fully idempotent when
    # run repeatedly in a development environment.
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"[INFO]  Removed existing database: {db_path}")

    print(f"[INFO]  Creating database: {db_path}")

    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()

        # Enable foreign-key constraint enforcement (off by default in SQLite).
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Create tables in dependency order.
        for table_name, ddl in TABLES:
            cursor.execute(ddl)
            print(f"[OK]    Table created: {table_name}")

        connection.commit()
        print("\n[INFO]  All tables committed successfully.")

        # Print schema summary for verification.
        print_schema_summary(cursor)

    except sqlite3.Error as exc:
        connection.rollback()
        print(f"[ERROR] Database error: {exc}")
        raise
    finally:
        connection.close()
        print(f"[INFO]  Connection closed. Database saved to: {os.path.abspath(db_path)}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    create_database()
