import os

import requests
import jwt
import datetime
from dotenv import load_dotenv
from functools import wraps
from flask import request

load_dotenv()

# Generate the JWT token
def generate_jwt():
    payload = {
        "data": "Approved",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token

# decorator for the middleware process, i.e., the verification
def verify_decorator(f):
    @wraps(f)
    def user_verification(*args, **kwargs):
        access_token = request.headers.get('accessToken')
        try:
            get_user_data = jwt.decode(access_token, options={"verify_signature": False})
            if(get_user_data["data"] == "Approved"):
                return f(True, *args, **kwargs)
        except Exception as e:            
            return {"data": "Authentication Failed!", "error": str(e), "status_code": 401}, 401      

        return {"data": "Authentication Failed!", "error": "Token Invalid!", "status_code": 401}, 401  

    return user_verification