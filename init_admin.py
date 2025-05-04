# app/init_admin.py
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import User
from passlib.hash import bcrypt

def create_admin():
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter_by(username="admin@gvam.local").first():
            hashed = bcrypt.hash("admin123")
            admin = User(username="admin@gvam.local", password=hashed, role="admin")
            db.add(admin)
            db.commit()
    finally:
        db.close()
