import requests
import os

tenant_id = "9ac50357-7ce0-4d4f-83d3-d8a10c328c05"
# my newly created tech account
client_id = "e38331db-660d-4604-94b2-b4fdcec9ca98"
scope = "https://graph.microsoft.com/.default"
# scope = "api://e38331db-660d-4604-94b2-b4fdcec9ca98/.default"

token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": scope,
    "grant_type": "client_credentials"
}

response = requests.post(token_url, data=data)
token = response.json().get("access_token")

print("Access Token:", token)


headers = {"Authorization": f"Bearer {token}"}
graph_url = "https://graph.microsoft.com/v1.0/users"

response = requests.get(graph_url, headers=headers)
users = response.json()

for user in users.get("value", []):
    print(f"Display Name: {user['displayName']}, UPN: {user['userPrincipalName']}")
