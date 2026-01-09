from ariadne import QueryType, MutationType
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import authenticate
from app.utils.jwt import create_token
from app.models import User
import jwt
from app.utils.jwt import SECRET_KEY, ALGORITHM

query = QueryType()
mutation = MutationType()

@mutation.field("login")
def resolve_login(_, info, email, password):
    db: Session = SessionLocal()
    user = authenticate(db, email, password)
    if not user:
        raise Exception("Invalid credentials")
    return {"accessToken": create_token(user)}

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