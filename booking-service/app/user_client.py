import httpx

USER_SERVICE_URL = "http://user-service:8000/graphql/"

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

    async with httpx.AsyncClient() as client:
        res = await client.post(
            USER_SERVICE_URL,
            json={"query": query, "variables": {"token": token}},
            headers={"Content-Type": "application/json"}   # <-- WAJIB
        )

        print("STATUS:", res.status_code)
        print("BODY:", res.text)

        data = res.json()

        if "errors" in data:
            raise Exception("Unauthorized")

        return data["data"]["validateToken"]
