"""Create or update a local administrator account.

Usage: python scripts/create_user.py --username admin --email admin@example.com
"""
from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import db
from app.security import ensure_user_table, hash_password


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a BBQ Analytics user")
    parser.add_argument("--username", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", default="Administrator")
    parser.add_argument("--role", default="Administrator")
    parser.add_argument("--title", default="Account Manager")
    args = parser.parse_args()
    password = getpass.getpass("Password: ")
    if len(password) < 12:
        parser.error("password must contain at least 12 characters")
    if password != getpass.getpass("Confirm password: "):
        parser.error("passwords do not match")
    ensure_user_table()
    db.execute_write(
        """INSERT INTO app_users (id, username, email, password_hash, name, role, title)
           VALUES (lower(hex(randomblob(16))), ?, ?, ?, ?, ?, ?)
           ON CONFLICT(username) DO UPDATE SET email=excluded.email, password_hash=excluded.password_hash,
             name=excluded.name, role=excluded.role, title=excluded.title""",
        (args.username.lower(), args.email.lower(), hash_password(password), args.name, args.role, args.title),
    )
    print(f"User '{args.username}' created or updated.")


if __name__ == "__main__":
    main()
