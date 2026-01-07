from ariadne import QueryType, MutationType
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import authenticate
from app.utils.jwt import create_token, SECRET_KEY, ALGORITHM
from app.models import User
from werkzeug.security import generate_password_hash
import jwt
import os 

query = QueryType()
mutation = MutationType()

EXTERNAL_URL = os.getenv("EXTERNAL_USER_SERVICE_URL")
# ======================
# MUTATIONS
# ======================

@mutation.field("register")
def resolve_register(_, info, email, password):
    db: Session = SessionLocal()

    # cek user sudah ada
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise Exception("User already exists")

    hashed_password = generate_password_hash(password)

    user = User(
        email=email,
        password=hashed_password,
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@mutation.field("login")
def resolve_login(_, info, email, password):
    db: Session = SessionLocal()
    user = authenticate(db, email, password)
    if not user:
        raise Exception("Invalid credentials")

    return {
        "accessToken": create_token(user)
    }


# ======================
# QUERIES
# ======================

@query.field("checkUserReputation")
def resolve_reputation(_, info, userId):
    db: Session = SessionLocal()
    user = db.query(User).get(int(userId))

    return {
        "score": user.reputation_score,
        "isBlacklisted": user.blacklisted
    }


@query.field("validateToken")
def resolve_validate_token(_, info, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "userId": payload["sub"],
            "email": payload["email"],
            "role": payload["role"]
        }
    except Exception:
        raise Exception("Invalid or expired token")

@query.field("me")
def resolve_me(_, info):
    request = info.context["request"]
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    token = auth_header.replace("Bearer ", "").strip()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None

    db: Session = SessionLocal()
    user = db.query(User).get(int(payload["sub"]))

    return user
