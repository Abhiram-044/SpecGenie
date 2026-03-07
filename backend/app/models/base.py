from bson import ObjectId
from pydantic import BaseModel, ConfigDict
from pydantic_core import core_schema

class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):

        def validate(value):
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")

            return ObjectId(value)

        return core_schema.no_info_plain_validator_function(validate)
    
class MongoBaseModel(BaseModel):
    id: PyObjectId | None = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )