import httpx
import asyncio

# === KONFIGURASI ===
URL = "https://kenzie-isauxetic-uncruelly.ngrok-free.dev/graphql"
USERNAME = "admin"
PASSWORD = "admin123"
VEHICLE_ID = "1"  # Gunakan String karena tipenya ID

async def debug_fixed_schema():
    print(f"🕵️  DEBUGGING BERDASARKAN SCHEMA VALID...")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        
        # ---------------------------------------------------
        # LANGKAH 1: LOGIN (Sesuai Schema: access_token)
        # ---------------------------------------------------
        print("[1] Melakukan Login...")
        login_query = """
        mutation ($username: String!, $password: String!) {
          login(username: $username, password: $password) {
            access_token
          }
        }
        """
        
        try:
            res = await client.post(URL, json={
                "query": login_query,
                "variables": {"username": USERNAME, "password": PASSWORD}
            })
            
            data = res.json()
            # Cek jika ada error
            if "errors" in data:
                print(f"❌ Login Error: {data['errors'][0]['message']}")
                return

            token = data.get("data", {}).get("login", {}).get("access_token")
            if not token:
                print("❌ Token tidak ditemukan.")
                return
                
            print(f"✅ Login Sukses! Token: {token[:10]}...")
            
        except Exception as e:
            print(f"❌ Exception Login: {e}")
            return

        # ---------------------------------------------------
        # LANGKAH 2: GET VEHICLE BY ID (Sesuai Schema)
        # ---------------------------------------------------
        print(f"\n[2] Mengambil Data Vehicle ID: {VEHICLE_ID}...")
        
        # Perhatikan: id bertipe ID! (bukan Int)
        vehicle_query = """
        query ($id: ID!) {
          getVehicleById(id: $id) {
            id
            model
            plateNumber
            status       # <--- INI KUNCINYA
            dailyPrice
          }
        }
        """
        
        try:
            res = await client.post(
                URL,
                json={
                    "query": vehicle_query,
                    "variables": {"id": VEHICLE_ID}
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            
            print(f"Status Code: {res.status_code}")
            print(f"RAW Response: {res.text}")
            
            data = res.json()
            if "errors" in data:
                print(f"❌ Error Query: {data['errors'][0]['message']}")
            else:
                vehicle = data.get("data", {}).get("getVehicleById")
                if vehicle:
                    print("-" * 40)
                    print(f"🚗 Model  : {vehicle['model']}")
                    print(f"🔢 Plat   : {vehicle['plateNumber']}")
                    print(f"💰 Harga  : {vehicle['dailyPrice']}")
                    print(f"✅ STATUS : {vehicle['status']}")  # <--- Perhatikan output ini
                    print("-" * 40)
                    
                    # LOGIKA SIMULASI UNTUK KODINGAN UTAMA NANTI
                    status_str = str(vehicle['status']).lower()
                    if status_str in ["available", "ready", "idle"]:
                        print("KESIMPULAN: Mobil TERSEDIA untuk dipesan.")
                    else:
                        print("KESIMPULAN: Mobil TIDAK TERSEDIA.")
                else:
                    print("❌ Data mobil null (Mungkin ID salah).")

        except Exception as e:
            print(f"❌ Exception Query: {e}")

if __name__ == "__main__":
    asyncio.run(debug_fixed_schema())