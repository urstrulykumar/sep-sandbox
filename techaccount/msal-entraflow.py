import msal
from requests import session as reqSession
from trino.auth import JWTAuthentication, OAuth2Authentication
from pystarburst import Session
import os

# client_id = "19486516-074e-479c-98f7-631df0b23a46"
tenant_id = os.getenv("client_secret")


# my newly created tech account
client_id = "e38331db-660d-4604-94b2-b4fdcec9ca98"
client_secret = os.getenv("secret")


authority = f"https://login.microsoftonline.com/{tenant_id}"
app = msal.ConfidentialClientApplication(client_id, client_secret, authority=authority)

token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in token_response:
    print("Access Token:", token_response["access_token"])
else:
    print("Failed to acquire token:", token_response.get("error_description"))
token = token_response["access_token"]
session = reqSession()
# session.headers.update({'Authorization': f'Bearer {token}'})
session.verify = False
db_parameters = {
    "host" : "localhost",
    "port" : "8443",
    "http_scheme" : "https",
    "http_session" : session,
    "verify" : False,
    # "auth" : OAuth2Authentication(),
    "auth" : JWTAuthentication(token),
    # "roles" : {"system" : "ROLE{sysadmin}"}
}
session = Session.builder.configs(db_parameters).create()
df = session.sql("select * from tpch.sf1.customer limit 10")
print(df.to_pandas().head)
