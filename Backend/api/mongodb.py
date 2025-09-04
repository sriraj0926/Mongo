from fastapi import APIRouter, HTTPException, Form
from bson import ObjectId
from Backend.db import get_db

mongodb_router = APIRouter()

@mongodb_router.post("/create_db/{db_name}")
async def create_db(db_name: str):
    db = get_db(db_name)
    # create a placeholder collection (forces DB creation)
    await db["__init__"].insert_one({"created": True})
    return {"message": f"Database '{db_name}' created"}


@mongodb_router.post("/{db_name}/collections/")
async def create_collection(db_name: str, collection_name: str = Form(...)):
    db = get_db(db_name)
    try:
        await db.create_collection(collection_name)
        return {"message": f"Collection '{collection_name}' created in '{db_name}'"}
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"Collection '{collection_name}' already exists in '{db_name}'"
            )
        raise HTTPException(status_code=500, detail=str(e))


@mongodb_router.post("/{db_name}/collections/{collection_name}/subitems")
async def add_subitem(
    db_name: str,
    collection_name: str,
    name: str = Form(...),
    age: int = Form(...),
    city: str = Form(...)
):
    db = get_db(db_name)
    result = await db[collection_name].insert_one({
        "name": name,
        "age": age,
        "city": city
    })
    return {
        "id": str(result.inserted_id),
        "message": f"Subitem added to '{collection_name}' in '{db_name}'"
    }


@mongodb_router.get("/{db_name}/collections/{collection_name}/subitems")
async def get_subitems(db_name: str, collection_name: str):
    db = get_db(db_name)
    subitems = []
    cursor = db[collection_name].find()
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        subitems.append(doc)
    return subitems

@mongodb_router.delete("/{db_name}/collections/{collection_name}/subitems/{item_id}")
async def delete_subitem(db_name: str, collection_name: str, item_id: str):
    db = get_db(db_name)
    result = await db[collection_name].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subitem not found")
    return {"message": f"Subitem deleted from '{collection_name}' in '{db_name}'"}
