from jose import jwt
from datetime import datetime, timedelta

SECRET = "secretkey"

def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=1)})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")