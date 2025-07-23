#!/usr/bin/env python3
"""
Database backup and restore utility for Ziply app
Usage:
  python backup_db.py backup    # Create backup
  python backup_db.py restore   # Restore from backup
"""

import sqlite3
import shutil
import os
import sys
from datetime import datetime

DB_FILE = "ziply.db"
BACKUP_DIR = "db_backups"

def create_backup():
    """Create a timestamped backup of the database"""
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found!")
        return False
    
    # Create backup directory if it doesn't exist
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Create timestamped backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"ziply_backup_{timestamp}.db")
    
    # Copy database file
    shutil.copy2(DB_FILE, backup_file)
    print(f"✅ Database backed up to: {backup_file}")
    return True

def restore_backup(backup_file=None):
    """Restore database from backup"""
    if not backup_file:
        # Find the most recent backup
        if not os.path.exists(BACKUP_DIR):
            print("No backup directory found!")
            return False
        
        backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
        if not backups:
            print("No backup files found!")
            return False
        
        # Get most recent backup
        backups.sort(reverse=True)
        backup_file = os.path.join(BACKUP_DIR, backups[0])
    
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} not found!")
        return False
    
    # Create backup of current database before restoring
    if os.path.exists(DB_FILE):
        current_backup = f"{DB_FILE}.pre_restore"
        shutil.copy2(DB_FILE, current_backup)
        print(f"Current database backed up to: {current_backup}")
    
    # Restore from backup
    shutil.copy2(backup_file, DB_FILE)
    print(f"✅ Database restored from: {backup_file}")
    return True

def list_backups():
    """List available backups"""
    if not os.path.exists(BACKUP_DIR):
        print("No backup directory found!")
        return
    
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
    if not backups:
        print("No backup files found!")
        return
    
    print("Available backups:")
    for backup in sorted(backups, reverse=True):
        backup_path = os.path.join(BACKUP_DIR, backup)
        size = os.path.getsize(backup_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        print(f"  {backup} ({size} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backup_db.py [backup|restore|list]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        create_backup()
    elif command == "restore":
        backup_file = sys.argv[2] if len(sys.argv) > 2 else None
        restore_backup(backup_file)
    elif command == "list":
        list_backups()
    else:
        print("Unknown command. Use: backup, restore, or list")
        sys.exit(1)
