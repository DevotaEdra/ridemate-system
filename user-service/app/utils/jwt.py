import jwt
from datetime import datetime, timedelta

SECRET_KEY = "RIDEMATE_SECRET"
ALGORITHM = "HS256"

def create_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
