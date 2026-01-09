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
    if not auth: raise Exception("Authorization header missing")
    token = auth.replace("Bearer ", "")
    
    try:
        user = await validate_token(token)
    except:
        raise Exception("Authentication Failed")

    db = SessionLocal()
    try:
        v_id_int = int(vehicleId)
        
        existing_booking = db.query(Booking).filter(
            Booking.vehicle_id == v_id_int,
            Booking.booking_date == date
        ).first()

        if existing_booking:
            raise Exception(f"GAGAL: Tanggal {date} sudah penuh (tercatat di Database Lokal).")
        
        is_available_external = await check_availability(vehicleId, date)
        
        if not is_available_external:
            raise Exception("GAGAL: Provider kendaraan menolak (Mobil tidak tersedia/sedang dipakai).")
        booking = Booking(
            user_id=int(user["userId"]),
            vehicle_id=v_id_int,
            booking_date=date,
            status="CONFIRMED"
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return {
            "id": booking.id,
            "user_id": booking.user_id,      
            "vehicle_id": booking.vehicle_id, 
            "booking_date": booking.booking_date, 
            "status": booking.status
        }
 
    except Exception as e:
        db.rollback() 
        raise e       
    finally:
        db.close()