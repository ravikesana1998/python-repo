from datetime import datetime
from pymongo import ReturnDocument
from app.database import database

class MasterMongo:
    def __init__(self, collection_name: str):
        """Initialize with a collection"""
        self.collection = database[collection_name]

    async def insert(self, data: dict):
        """Insert a document with created_date"""
        data["created_at"] = str(datetime.utcnow())
        data["updated_at"] = str(datetime.utcnow())
        data["created_by"] = data["user_id"]
        data["updated_by"] = data["user_id"]
        result = await self.collection.insert_one(data)
        del data["_id"]
        return data

    async def update(self, filter_query: dict, update_data: dict):
        """Update a document and set updated_date"""
        update_data["updated_at"] = str(datetime.utcnow())
        update_data["updated_by"] = update_data["user_id"]
        result = await self.collection.find_one_and_update(
            filter_query,
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        return result

    async def find_one(self, filter_query: dict, projection: dict = {}):
        """Find a single document with optional projection"""
        projection["_id"] = 0  # Exclude _id field
        document = await self.collection.find_one(filter_query, projection)
        return document

    async def find_many(self, filter_query: dict, projection: dict = {}):
        """Find multiple documents with optional projection"""
        projection["_id"] = 0  # Exclude _id field
        cursor = self.collection.find(filter_query, projection)
        documents = await cursor.to_list(length=100)  # Adjust limit as needed
        return documents
    
    async def delete(self, filter_query: dict):
        """Delete a document"""
        return await self.collection.delete_one(filter_query)
