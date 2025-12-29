from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from .models import User

def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and bcrypt.verify(password, user.password):
        return user
    return None
