from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="customer")
    reputation_score = Column(Integer, default=100)
    blacklisted = Column(Boolean, default=False)
