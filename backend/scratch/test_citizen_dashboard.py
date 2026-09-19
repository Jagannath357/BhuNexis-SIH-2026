import httpx
from app.core.security import create_access_token

token = create_access_token(subject=1, role="CITIZEN", email="citizen@bhunexis.gov.in")
headers = {"Authorization": f"Bearer {token}"}
response = httpx.get("http://127.0.0.1:8000/api/v1/dashboard/citizen", headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json() if response.status_code == 200 else response.text)
