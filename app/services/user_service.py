from app.master_mongo import MasterMongo
import uuid
from fastapi import HTTPException

user_collection = MasterMongo("users")

async def save_user_id(user_data):
    """Save only user_id in MongoDB"""
    try:
        user_data["user_id"] = str(uuid.uuid4())
        inserted_id = await user_collection.insert(user_data)
        return inserted_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving user ID: {str(e)}")

async def get_user_by_id(user_id: str):
    """Fetch user by user_id"""
    try:
        return await user_collection.find_one({"user_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user by ID: {str(e)}")

async def get_all_users_from_mongo():
    """Fetch all users from MongoDB"""
    try:
        return await user_collection.find_many({})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all users: {str(e)}")
    
