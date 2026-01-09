import os
import httpx

AVAILABILITY_SERVICE_URL = "https://kenzie-isauxetic-uncruelly.ngrok-free.dev/availability/graphql/"

async def check_availability(vehicle_id: str, date: str) -> bool:
    """
    Mengecek ketersediaan kendaraan ke Availability Service Kelompok Lain.
    Query: checkAvailability(vehicleId, date)
    Auth: Tidak diperlukan (Public Endpoint)
    """
    
    query = """
    query ($vehicleId: Int!, $date: String!) {
      checkAvailability(vehicleId: $vehicleId, date: $date)
    }
    """
    
    variables = {
        "vehicleId": vehicle_id, 
        "date": date
    }

    print(f"📡 [FleetClient] Mengecek Availability...")
    print(f"   URL: {AVAILABILITY_SERVICE_URL}")
    print(f"   Vehicle ID: {vehicle_id}, Date: {date}")

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(
                AVAILABILITY_SERVICE_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )
            
            
            data = response.json()
            if "errors" in data:
                print(f"❌ [FleetClient] Error dr Server Sebelah: {data['errors'][0]['message']}")
                return False

            raw_response = data.get("data", {}).get("checkAvailability")
            
            print(f"🔍 [DEBUG PENTING] Respon Asli: '{raw_response}' (Tipe: {type(raw_response)})")
            
            if raw_response is None:
                return False

            status_str = str(raw_response).upper().strip()

            POSITIVE_ANSWERS = ["AVAILABLE"]

            if status_str in POSITIVE_ANSWERS:
                print("✅ Kesimpulan: MOBIL TERSEDIA")
                return True
            else:
                print(f"⚠️ Kesimpulan: DITOLAK (Status '{status_str}' tidak ada di daftar whitelist)")
                return False

        except Exception as e:
            print(f"❌ Error Koneksi: {e}")
            return False