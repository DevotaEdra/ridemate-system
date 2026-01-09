import os
import httpx

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000/graphql")

async def validate_token(token: str):
    query = """
    query ($token: String!) {
      validateToken(token: $token) {
        userId
        email
        role
      }
    }
    """

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

        if res.status_code != 200:
            print(f"User Service Error [{res.status_code}]: {res.text}")
            raise Exception("Authentication Service Error")

        data = res.json()

        if "errors" in data:
            print("GraphQL Errors:", data["errors"])
            raise Exception("Unauthorized")

        return data["data"]["validateToken"]