from app.security import hash_password
from app import db
import uuid

def create_user():
    db.execute_write(
        '''CREATE TABLE IF NOT EXISTS app_users (
            id TEXT PRIMARY KEY, 
            username TEXT NOT NULL UNIQUE, 
            email TEXT NOT NULL UNIQUE, 
            password_hash TEXT NOT NULL, 
            name TEXT NOT NULL, 
            role TEXT NOT NULL DEFAULT 'Manager', 
            title TEXT NOT NULL DEFAULT 'Restaurant Manager', 
            status TEXT NOT NULL DEFAULT 'Active', 
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )'''
    )
    pw_hash = hash_password('iba@123')
    user_id = str(uuid.uuid4())
    try:
        db.execute_write(
            'INSERT INTO app_users (id, username, email, password_hash, name, role) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, 'waseem', 'waseem@example.com', pw_hash, 'Waseem', 'Admin')
        )
        print('User created successfully.')
    except Exception as e:
        print('Error:', e)

create_user()
