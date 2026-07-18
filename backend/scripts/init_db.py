#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables in the database for both SQLite and PostgreSQL.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.database.init_db import init_db

def main():
    """Initialize the database."""
    print("Initializing database...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()