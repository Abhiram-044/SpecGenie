from typing import Any, Dict
from pydantic import BaseModel
from app.models.base import PyObjectId
from bson import ObjectId
from app.utils.resume_helpers import serialize_for_mongo

def get_top_level_update_query(field_name: str, schema_data: BaseModel) -> Dict[str, Any]:
    update_data = schema_data.model_dump(exclude_none=True)
    update_data = serialize_for_mongo(update_data)

    return {
        "$set": {
            f"{field_name}.{k}": v for k, v in update_data.items()
        }
    }

def get_update_query(schema_data: BaseModel) -> Dict[str, Any]:
    update_data = schema_data.model_dump(exclude_none=True)

    return {
        "$set": {
            f"{k}": v for k, v in update_data.items()
        }
    }

def get_array_item_update_query(
        list_field: str,
        item_id: str | PyObjectId,
        schema_data: BaseModel
) -> Dict[str, Any]:
    update_data = schema_data.model_dump(exclude_unset=True)
    update_data = serialize_for_mongo(update_data)

    set_query = {f"{list_field}.$[elem].{k}": v for k, v in update_data.items() if k != "id"}

    return {
        "update_filter": {"_id": ObjectId(item_id) if isinstance(item_id, str) else item_id},
        "set_query": {"$set": set_query},
        "array_filters": [{"elem._id": ObjectId(item_id) if isinstance(item_id, str) else item_id}]
    }