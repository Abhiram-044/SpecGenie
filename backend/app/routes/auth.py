from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.schemas.auth_schema import RegistrationIntiate, RegistrationComplete, TokenResponse
from app.database.mongodb import get_database
from app.database.redis import get_redis
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth_dependency import get_current_user
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register/initiate")
async def initiate_registration(data: RegistrationIntiate):
    db = get_database()
    redis_client = get_redis()

    if await db.users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    magic_token = str(uuid.uuid4())

    await redis_client.set(f"reg_token: {magic_token}", data.email, ex=1200)

    return {
        "success": True,
        "message": "Token generated",
        "magic_token": magic_token
    }

@router.post("/register/complete/{magic_token}")
async def complete_registration(magic_token: str, data: RegistrationComplete):
    db = get_database()
    redis_client = get_redis()
    
    email = await redis_client.get(f"reg_token: {magic_token}")

    if not email:
        raise HTTPException(400, "Invalid or expired token")

    if data.password != data.confirm_password:
        raise HTTPException(401, "Password Mismatch")
    
    if await db.users_collection.find_one({"username": data.username}):
        raise HTTPException(401, "Username already exist. Enter Another")

    user_doc = User(
        email=email,
        username=data.username,
        hashed_password=hash_password(data.password),
        latest_session_id=None
    )

    user = await db.users_collection.insert_one(
        user_doc.model_dump(by_alias=True, exclude={"id"})
    )

    await redis_client.delete(f"reg_token: {magic_token}")

    return {
        "success": True,
        "message": "Account created succesfully"
    }

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()

    user = await db.users_collection.find_one({
        "$or": [{"email": form_data.username}, {"username": form_data.username}]
    })

    if not user:
        raise HTTPException(401, "User does not exist. Regiter new user")
    
    if not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(401, "Incorrect password. Try Again")
    
    new_session_id = str(uuid.uuid4())
    
    token = create_access_token(str(user["_id"]), new_session_id)

    await db.users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "latest_session_id": new_session_id,
            "is_active": True
        }}
    )

    return {
        "success": True,
        "access_token": token
    }

@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    db = get_database()

    await db.users_collection.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {
                "latest_session_id": None,
                "is_active": False      
            }}
        )

    return {
        "success": True,
        "message": "Logged out successfully"
    }

@router.get("me")
async def get_me(user=Depends(get_current_user)):
    return {
        "success": True,
        "user": {
            "id": user["_id"],
            "email": user["email"],
            "username": user["username"]
        }   
    }