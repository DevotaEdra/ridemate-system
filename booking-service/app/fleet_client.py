import os
import httpx

# Konfigurasi Environment
VEHICLE_SERVICE_URL = os.getenv("VEHICLE_SERVICE_URL", "https://kenzie-isauxetic-uncruelly.ngrok-free.dev/graphql")
USERNAME = os.getenv("EXTERNAL_LOGIN_USERNAME", "admin") 
PASSWORD = os.getenv("EXTERNAL_LOGIN_PASSWORD", "admin123")

CACHED_TOKEN = None

async def login_to_vehicle_service():
    global CACHED_TOKEN
    # Query login sesuai spesifikasi teman Anda (access_token)
    mutation = """
    mutation ($username: String!, $password: String!) {
      login(username: $username, password: $password) {
        access_token 
      }
    }
    """
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            res = await client.post(
                VEHICLE_SERVICE_URL,
                json={"query": mutation, "variables": {"username": USERNAME, "password": PASSWORD}}
            )
            token = res.json().get("data", {}).get("login", {}).get("access_token")
            if token: CACHED_TOKEN = token
            return token
        except:
            return None

async def check_availability(vehicle_id: str) -> bool:
    """
    Hanya mengecek status fisik mobil.
    Return True jika status == 'active'.
    """
    global CACHED_TOKEN
    
    # Auto Login Logic
    if CACHED_TOKEN is None:
        if await login_to_vehicle_service() is None: return False

    async def send_request(token):
        # Kita minta 'status' mobil
        query = """
        query ($id: ID!) {
          getVehicleById(id: $id) {
            id
            status
          }
        }
        """
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            return await client.post(
                VEHICLE_SERVICE_URL,
                json={"query": query, "variables": {"id": vehicle_id}},
                headers={"Authorization": f"Bearer {token}"}
            )

    try:
        res = await send_request(CACHED_TOKEN)
    except:
        return False

    # Refresh Token jika expired (401)
    if res.status_code in [401, 403]:
        if await login_to_vehicle_service():
            res = await send_request(CACHED_TOKEN)
        else:
            return False

    if res.status_code == 200:
        data = res.json()
        vehicle = data.get("data", {}).get("getVehicleById")
        
        if not vehicle: return False # Mobil tidak ditemukan
        
        # LOGIKA BARU: Cek apakah status == "active"
        status = str(vehicle.get("status", "")).lower()
        
        print(f"DEBUG: Status Mobil ID {vehicle_id} adalah '{status}'")
        
        if status == "active":
            return True
            
    return False