from datetime import date, datetime

def serialize_for_mongo(obj):
    """
    Recursively converts unsupported Mongo types.
    Currently converts datetime.date -> datetime.datetime
    """
    if isinstance(obj, dict):
        return {k: serialize_for_mongo(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [serialize_for_mongo(v) for v in obj]

    if isinstance(obj, date) and not isinstance(obj, datetime):
        return datetime.combine(obj, datetime.min.time())

    return obj

def remove_empty_fields(data):
    if isinstance(data, dict):
        return {
            k: remove_empty_fields(v)
            for k, v in data.items()
            if v not in (None, "", []) and remove_empty_fields(v) != {}
        }

    if isinstance(data, list):
        cleaned_list = [remove_empty_fields(item) for item in data]
        return [item for item in cleaned_list if item not in (None, "", {}, [])]

    return data