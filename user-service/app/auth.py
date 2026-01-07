from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
from app.models import User


def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not check_password_hash(user.password, password):
        return None

    return user
