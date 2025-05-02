from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.user_schema import UserCreate
from app.services.user_service import save_user_id, get_user_by_id, get_all_users_from_mongo

router = APIRouter()

@router.post("/add_user", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def add_user(user: UserCreate):
    """Save only user_id to MongoDB with timestamps"""

    user_dict = user.model_dump()
    inserted_id = await save_user_id(user_dict)
    if not inserted_id:
        raise HTTPException(status_code=500, detail="Failed to save user ID")

    return JSONResponse(content={"message": "User ID saved successfully", "data": inserted_id})

@router.get("/get_user/{user_id}", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def get_user(user_id: str):
    """Get user by user_id from MongoDB"""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(content={"message": "User found", "data": user})

@router.get("/get_all_users", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def get_all_users():
    """Get all users from MongoDB"""
    users = await get_all_users_from_mongo()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return JSONResponse(content={"message": "Users found", "data": users})