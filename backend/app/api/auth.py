from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserLogin
from app.db.database import users_collection
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/signup")
async def signup(user: UserCreate):

    existing_user = await users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    new_user = {
        "email": user.email,
        "password": hashed_password
    }

    result = await users_collection.insert_one(new_user)

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    }


@router.post("/login")
async def login(user: UserLogin):

    db_user = await users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": str(db_user["_id"])})

    return {"access_token": token}