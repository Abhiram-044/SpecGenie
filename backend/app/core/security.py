from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

pwd_content = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_content.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    return pwd_content.verify(
        plain_password,
        hashed_password
    )

def create_access_token(user_id: str, session_id: str):
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": user_id,
        "sid": session_id,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_token(token: str):

    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )

    user_id: str = payload.get("sub")
    session_id: str = payload.get("sid")

    if user_id is None:
        raise Exception("Invalid token payload")

    return {
        "user_id": user_id,
        "session_id": session_id
    }