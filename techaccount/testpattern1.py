from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
from pystarburst import Session
from trino.auth import JWTAuthentication, OAuth2Authentication
from trino.dbapi import connect
import urllib3 as urlib
import jwt
from requests import session as reqSession
from dotenv import load_dotenv
import time
import os

class AccessToken:
    urlib.disable_warnings()
    load_dotenv()
    token = ""

    def __init__(self):
        self.client_id = os.getenv("client_id")
        self.tenant_id = os.getenv("tenant_id")
        self.scope = os.getenv("scope")
        
    def getCatalogData(self):
        sbsession = self.getSBSession()
        df = sbsession.sql("select * from tpch.sf1.customer limit 10")
        print(df.to_pandas().head)

    def getAccessToken(self):
        print(f"Checking token {self.token}")
        if self.token != "":
            print("Token is expired. Generating new one")
        else:
            print(f"token is empty {self.token}")
            credential = ClientSecretCredential(tenant_id = self.tenant_id, 
                                                client_id = self.client_id,
                                                client_secret = self.secret)
            # credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
            self.token = credential.get_token(self.scope).token
            print(self.token)

    def getSBSession(self):
        # self.updateToken()
        session = reqSession()
        session.headers.update({'Authorization': f'Bearer {self.token}'})
        session.verify = False
        db_parameters = {
            "host" : "localhost",
            "port" : "8443",
            "http_scheme" : "https",
            "http_session" : session,
            "verify" : False,
            # "auth" : OAuth2Authentication(),
            "auth" : JWTAuthentication(self.token),
            # "roles" : {"system" : "ROLE{sysadmin}"}
        }
        session = Session.builder.configs(db_parameters).create()
        return session
    
    def updateToken(self):
        decoded_payload = jwt.decode(self.token, options={"verify_signature": False})
        print("Decoded Token: ", decoded_payload)
        # Replace 'sub' with 'upn'
        if "sub" in decoded_payload:
            decoded_payload["upn"] = decoded_payload.pop("sub")

        print(self.secret)
        # Re-encode the JWT
        new_token = jwt.encode(decoded_payload, self.secret, algorithm="HS256")

        # self.token = new_token

        print("Updated JWT:", decoded_payload)
        print("Updated token:", new_token)
    

token = AccessToken()
accesstoken = token.getAccessToken()
# token.updateToken()
token.getCatalogData()

