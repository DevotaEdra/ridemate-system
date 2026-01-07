from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL database untuk container Docker
DATABASE_URL = "postgresql://user:password@booking-db:5432/db_booking"

# Engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class untuk model ORM
Base = declarative_base()
