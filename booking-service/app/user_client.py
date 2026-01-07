import os
import httpx

# Ambil URL dari Environment Variable
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000/graphql")

async def validate_token(token: str):
    # Query Internal User Service (Milik Sendiri)
    query = """
    query ($token: String!) {
      validateToken(token: $token) {
        userId
        email
        role
      }
    }
    """

    # UPDATE: Tambahkan 'follow_redirects=True' agar tidak error 307
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            res = await client.post(
                USER_SERVICE_URL,
                json={"query": query, "variables": {"token": token}},
                headers={"Content-Type": "application/json"}
            )
        except httpx.RequestError as e:
            print(f"Connection Error to User Service: {e}")
            raise Exception("Internal Service Unavailable")

        # Debugging: Print jika status bukan 200
        if res.status_code != 200:
            print(f"User Service Error [{res.status_code}]: {res.text}")
            raise Exception("Authentication Service Error")

        data = res.json()

        if "errors" in data:
            print("GraphQL Errors:", data["errors"])
            raise Exception("Unauthorized")

        return data["data"]["validateToken"]