import os
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Optional
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()


password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "H256")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY env var is not set")

VERIFICATION_TOKEN_EXPIRE_HOURS = int(os.getenv("VERIFICATION_TOKEN_EXPIRE_HOURS", "24"))

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_verification_token(user_id:str):
    # generate JWT token for email verification
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire,
        "type": "email_verification",
    }

    return jwt.encode(payload, 
                      SECRET_KEY,
                      algorithm=ALGORITHM)

def verify_email_token(token: str) -> Optional[int]:
    try:
        #algorithms must be a list [ALGORITHM]
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        print(f"DEBUG: Decoded Payload: {payload}")
        if payload.get("type") != "email_verification":
            return None
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            print("DEBUG: Type mismatch!")
            return None

        return int(user_id_str)
    except jwt.ExpiredSignatureError:
        print("DEBUG: Token expired!")
        return "expired"
    except jwt.PyJWTError as e:
        print(f"DEBUG: JWT Error: {e}")
        return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)