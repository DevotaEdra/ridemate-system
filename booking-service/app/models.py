from sqlalchemy import Column, Integer, String
from .database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    vehicle_id = Column(String, nullable=False)
    booking_date = Column(String, nullable=False)
    status = Column(String, default="CONFIRMED")
