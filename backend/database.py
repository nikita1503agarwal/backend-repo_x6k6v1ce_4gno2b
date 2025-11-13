import os
from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "event_storyboard")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    res = await db[collection_name].insert_one(data)
    doc = await db[collection_name].find_one({"_id": res.inserted_id})
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc or {}

async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    results: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        results.append(doc)
    return results

async def get_document(collection_name: str, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = await get_db()
    doc = await db[collection_name].find_one(filter_dict)
    if not doc:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc

async def update_document(collection_name: str, filter_dict: Dict[str, Any], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = await get_db()
    await db[collection_name].update_one(filter_dict, {"$set": data})
    return await get_document(collection_name, filter_dict)

async def delete_document(collection_name: str, filter_dict: Dict[str, Any]) -> bool:
    db = await get_db()
    res = await db[collection_name].delete_one(filter_dict)
    return res.deleted_count == 1
