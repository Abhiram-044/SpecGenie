from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from app.core.security import decode_token
from app.database.mongodb import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):

    user_details = decode_token(token)
    db = get_database()

    user = await db.users_collection.find_one({
        "_id": ObjectId(user_details["user_id"])
    })

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    if user_details["session_id"] != user["latest_session_id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Login Again"
        )

    user["_id"] = str(user["_id"])
    return user