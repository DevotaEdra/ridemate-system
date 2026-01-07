from ariadne import QueryType, MutationType
from app.database import SessionLocal
from app.models import Booking
from app.user_client import validate_token
from app.fleet_client import check_availability

query = QueryType()
mutation = MutationType()

@query.field("myBookings")
async def resolve_my_bookings(_, info):
    request = info.context["request"]
    auth = request.headers.get("Authorization")

    if not auth:
        raise Exception("Authorization header missing")

    token = auth.replace("Bearer ", "").strip()
    user = await validate_token(token)

    db = SessionLocal()
    return db.query(Booking).filter(
        Booking.user_id == int(user["userId"])
    ).all()

@mutation.field("createBooking")
async def resolve_create_booking(_, info, vehicleId, date):
    request = info.context["request"]
    auth = request.headers.get("Authorization")

    if not auth:
        raise Exception("Authorization header missing")

    token = auth.replace("Bearer ", "")
    user = await validate_token(token)

    available = await check_availability(vehicleId)
    if not available:
        raise Exception("Vehicle not available")

    db = SessionLocal()
    booking = Booking(
        user_id=int(user["userId"]),
        vehicle_id=vehicleId,
        booking_date=date
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking
