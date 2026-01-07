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
    
    # 1. Validasi User
    try:
        user = await validate_token(token)
    except:
        raise Exception("Authentication Failed")

    db = SessionLocal()
    try:
        v_id_int = int(vehicleId)

        # ---------------------------------------------------------
        # 2. CEK DATABASE LOKAL (LOGIKA TANGGAL)
        # Karena External Service tidak peduli tanggal, kitalah yang 
        # harus menjaga agar tanggal ini tidak double booking.
        # ---------------------------------------------------------
        # ---------------------------------------------------
        # 2. CEK DATABASE LOKAL (LOGIKA SOFT FAIL)
        # ---------------------------------------------------
        existing_booking = db.query(Booking).filter(
            Booking.vehicle_id == v_id_int,
            Booking.booking_date == date
        ).first()

        if existing_booking:
            print(f"⚠️ Booking Ditolak: Tanggal {date} sudah terisi.")
            
            # --- REVISI DISINI ---
            return {
                "id": None,   # <--- Gunakan None (Python) -> null (GraphQL)
                "userId": int(user["userId"]),
                "vehicleId": v_id_int,
                "bookingDate": date,
                "status": f"GAGAL: Mobil sudah dibooking pada tanggal {date}"
            }

        # ---------------------------------------------------
        # 3. CEK EXTERNAL
        # ---------------------------------------------------
        is_active = await check_availability(vehicleId)
        
        if not is_active:
            # Return Gagal juga kalau mobil rusak
            return {
                "id": None,   # <--- Gunakan None
                "userId": int(user["userId"]),
                "vehicleId": v_id_int,
                "bookingDate": date,
                "status": "GAGAL: Mobil sedang tidak aktif/rusak (Cek Vehicle Service)"
            }
        # ---------------------------------------------------------
        # 4. SIMPAN (CREATE BOOKING)
        # Tanggal yang diinput user disimpan disini
        # ---------------------------------------------------------
        booking = Booking(
            user_id=int(user["userId"]),
            vehicle_id=v_id_int,
            booking_date=date,   # <--- Tanggal disimpan disini
            status="CONFIRMED"
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()