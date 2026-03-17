from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from bson import ObjectId
import json
from bson.errors import InvalidId
from fastapi.encoders import jsonable_encoder

from app.database.mongodb import get_database
from app.database.redis import get_redis
from app.dependencies.auth_dependency import get_current_user
from app.utils.mongo_update_builder import get_top_level_update_query, get_array_item_update_query, get_update_query
from app.utils.resume_helpers import serialize_for_mongo, remove_empty_fields
from app.services.s3_service import delete_object, upload_profile_picture, upload_signature as upload_signature_s3, generate_signed_url

from app.schemas import profile_schema

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("")
async def get_profile(user=Depends(get_current_user)):
    db = get_database()
    redis_client = get_redis()

    cache_key = f"profile:{user['_id']}"

    cached_profile = await redis_client.get(cache_key)

    if cached_profile:
        data =  json.loads(cached_profile)

        if data.get("profilePicture"):
            data["profilePicture"] = await generate_signed_url(data["profilePicture"])
        if data.get("declaration", {}).get("signature"):
            data["declaration"]["signature"] = await generate_signed_url(data["declaration"]["signature"])
        
        return {
            "success": True,
            "message": "Fetched Profile Data Successfully",
            "data": data
        }
    
    profile = await db.master_resume_collection.find_one({
        "user_id": ObjectId(user["_id"])
    })

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    serialized_profile = jsonable_encoder(
        profile,
        custom_encoder={ObjectId: str}
    )

    cleaned_profile = remove_empty_fields(serialized_profile)

    await redis_client.set(
        cache_key,
        json.dumps(cleaned_profile),
        ex=86400
    )

    if cleaned_profile.get("profilePicture"):
        cleaned_profile["profilePicture"] = await generate_signed_url(cleaned_profile["profilePicture"])
    if cleaned_profile.get("declaration", {}).get("signature"):
        cleaned_profile["declaration"]["signature"] = await generate_signed_url(cleaned_profile["declaration"]["signature"])

    return {
        "success": True,
        "message": "Fetched Profile Data Successfully",
        "data": cleaned_profile
    }

@router.patch("/personal-details")
async def update_personal_details(
    data: profile_schema.PersonalDetails,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()
    query = get_top_level_update_query("personalDetails", data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        query
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Personal details updated",
        "data": jsonable_encoder(dump_model)
    }

@router.post("/education-details")
async def add_education(
    data: profile_schema.EducationCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    education_doc = data.model_dump(by_alias=True)
    education_doc = serialize_for_mongo(education_doc)

    if "_id" not in education_doc:
        education_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "educationDetails": education_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    education_doc["_id"] = str(education_doc["_id"])

    cleaned_doc = remove_empty_fields(education_doc)

    return {
        "success": True,
        "message": "Education added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/education-details/{education_id}")
async def update_education(
    education_id: str,
    data: profile_schema.EducationUpdate,
    user=Depends(get_current_user)
):
    
    try:
        obj_id = ObjectId(education_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid education ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("educationDetails", education_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Education record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Education updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/education-details/{education_id}")
async def delete_education(
    education_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(education_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid education ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "educationDetails": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Education record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Education Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/skills")
async def add_skill(
    data: profile_schema.SkillCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    skill_doc = data.model_dump(by_alias=True)
    skill_doc = serialize_for_mongo(skill_doc)

    if "_id" not in skill_doc:
        skill_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "skills": skill_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")
    
    skill_doc["_id"] = str(skill_doc["_id"])

    cleaned_doc = remove_empty_fields(skill_doc)

    return {
        "success": True,
        "message": "Skill added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/skills/{skill_id}")
async def update_skill(
    skill_id: str,
    data: profile_schema.SkillUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(skill_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Skill ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("skills", skill_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Skill record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Skill updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(skill_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Skill ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "skills": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Skill record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Skill Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/professional-experiences")
async def add_experience(
    data: profile_schema.ProfessionalExpCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    profExp_doc = data.model_dump(by_alias=True)
    profExp_doc = serialize_for_mongo(profExp_doc)

    if "_id" not in profExp_doc:
        profExp_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "professionalExperiences": profExp_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    profExp_doc["_id"] = str(profExp_doc["_id"])

    cleaned_doc = remove_empty_fields(profExp_doc)

    return {
        "success": True,
        "message": "Experience added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/professional-experiences/{experience_id}")
async def update_experience(
    experience_id: str,
    data: profile_schema.ProfessionalExpUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(experience_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Experience ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("professionalExperiences", experience_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Experience record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Experience updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/professional-experiences/{experience_id}")
async def delete_experience(
    experience_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(experience_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid experience ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "professionalExperiences": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Experience record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Experience Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/languages")
async def add_language(
    data: profile_schema.LanguageCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    lang_doc = data.model_dump(by_alias=True)
    lang_doc = serialize_for_mongo(lang_doc)

    if "_id" not in lang_doc:
        lang_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "languages": lang_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    lang_doc["_id"] = str(lang_doc["_id"])

    cleaned_doc = remove_empty_fields(lang_doc)

    return {
        "success": True,
        "message": "Language added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/languages/{language_id}")
async def update_language(
    language_id: str,
    data: profile_schema.LanguageUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(language_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Language ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("languages", language_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Language record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Language updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/languages/{language_id}")
async def delete_language(
    language_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(language_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid language ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "languages": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Language record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Language Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/certificates")
async def add_certificate(
    data: profile_schema.CertificateCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    certi_doc = data.model_dump(by_alias=True)
    certi_doc = serialize_for_mongo(certi_doc)

    if "_id" not in certi_doc:
        certi_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "certificates": certi_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    certi_doc["_id"] = str(certi_doc["_id"])

    cleaned_doc = remove_empty_fields(certi_doc)

    return {
        "success": True,
        "message": "Certificate added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/certificates/{certificate_id}")
async def update_certificate(
    certificate_id: str,
    data: profile_schema.CertificateUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(certificate_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Certificate ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("certificates", certificate_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Certificate record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Certificate updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/certificates/{certificate_id}")
async def delete_certificate(
    certificate_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(certificate_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid certificate ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "certificates": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Certificate record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Certificate Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/projects")
async def add_project(
    data: profile_schema.ProjectCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    proj_doc = data.model_dump(by_alias=True)
    proj_doc = serialize_for_mongo(proj_doc)

    if "_id" not in proj_doc:
        proj_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "projects": proj_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    proj_doc["_id"] = str(proj_doc["_id"])

    cleaned_doc = remove_empty_fields(proj_doc)

    return {
        "success": True,
        "message": "Project added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/projects/{project_id}")
async def update_project(
    project_id: str,
    data: profile_schema.ProjectUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(project_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Project ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("projects", project_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Project record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Project updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(project_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid project ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "projects": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Project Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/awards")
async def add_award(
    data: profile_schema.AwardCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    award_doc = data.model_dump(by_alias=True)
    award_doc = serialize_for_mongo(award_doc)

    if "_id" not in award_doc:
        award_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "awards": award_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    award_doc["_id"] = str(award_doc["_id"])

    cleaned_doc = remove_empty_fields(award_doc)

    return {
        "success": True,
        "message": "Award added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/awards/{award_id}")
async def update_award(
    award_id: str,
    data: profile_schema.AwardUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(award_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Award ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("awards", award_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Award record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Award updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/awards/{award_id}")
async def delete_award(
    award_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(award_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid award ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "awards": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Award record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Award Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/courses")
async def add_course(
    data: profile_schema.CourseCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    course_doc = data.model_dump(by_alias=True)
    course_doc = serialize_for_mongo(course_doc)

    if "_id" not in course_doc:
        course_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "courses": course_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    course_doc["_id"] = str(course_doc["_id"])

    cleaned_doc = remove_empty_fields(course_doc)

    return {
        "success": True,
        "message": "Course added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/courses/{course_id}")
async def update_course(
    course_id: str,
    data: profile_schema.CourseUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(course_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Course ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("courses", course_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Course record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Course updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(course_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid course ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "courses": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Course record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Course Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/organizations")
async def add_organization(
    data: profile_schema.OrganizationCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    organization_doc = data.model_dump(by_alias=True)
    organization_doc = serialize_for_mongo(organization_doc)

    if "_id" not in organization_doc:
        organization_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "organizations": organization_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    organization_doc["_id"] = str(organization_doc["_id"])

    cleaned_doc = remove_empty_fields(organization_doc)

    return {
        "success": True,
        "message": "Organization added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/organizations/{organization_id}")
async def update_organization(
    organization_id: str,
    data: profile_schema.OrganizationUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(organization_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Organization ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("organizations", organization_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Organization record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Organization updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/organizations/{organization_id}")
async def delete_organization(
    organization_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(organization_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid organization ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "organizations": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Organization record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Organization Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/publications")
async def add_publication(
    data: profile_schema.PublicationCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    publication_doc = data.model_dump(by_alias=True)
    publication_doc = serialize_for_mongo(publication_doc)

    if "_id" not in publication_doc:
        publication_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "publications": publication_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    publication_doc["_id"] = str(publication_doc["_id"])

    cleaned_doc = remove_empty_fields(publication_doc)

    return {
        "success": True,
        "message": "Publication added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/publications/{publication_id}")
async def update_publication(
    publication_id: str,
    data: profile_schema.PublicationUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(publication_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Publication ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("publications", publication_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Publication record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Publication updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/publications/{publication_id}")
async def delete_publication(
    publication_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(publication_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid publication ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "publications": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Publication record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Publication Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.post("/references")
async def add_reference(
    data: profile_schema.ReferenceCreate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    reference_doc = data.model_dump(by_alias=True)
    reference_doc = serialize_for_mongo(reference_doc)

    if "_id" not in reference_doc:
        reference_doc["_id"] = ObjectId()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$push": {
            "references": reference_doc
        }},
        upsert=False
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    await redis_client.delete(f"profile:{user['_id']}")

    reference_doc["_id"] = str(reference_doc["_id"])

    cleaned_doc = remove_empty_fields(reference_doc)

    return {
        "success": True,
        "message": "Reference added",
        "data": jsonable_encoder(cleaned_doc)
    }

@router.patch("/references/{reference_id}")
async def update_reference(
    reference_id: str,
    data: profile_schema.ReferenceUpdate,
    user=Depends(get_current_user)
):
    
    try:
        ObjectId(reference_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Reference ID format")
    
    db = get_database()
    redis_client = get_redis()

    payload = get_array_item_update_query("references", reference_id, data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        payload["set_query"],
        array_filters=payload["array_filters"]
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, 
            detail="Reference record not found or no changes made"
        )

    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Reference updated",
        "data": jsonable_encoder(dump_model)
    }

@router.delete("/references/{reference_id}")
async def delete_reference(
    reference_id: str,
    user=Depends(get_current_user)
):
    try:
        obj_id = ObjectId(reference_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid reference ID format")
    
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {
            "$pull": {
                "references": {
                    "_id": obj_id
                }
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Reference record not found")
    
    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Reference Deleted",
        "data": {"deleted_id": str(obj_id)}
    }

@router.patch("/image")
async def upload_picture(file: UploadFile = File(...), user=Depends(get_current_user)):

    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(400, "Only PNG/JPG allowed")
    
    if file.size > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    
    db = get_database()
    redis_client = get_redis()

    resume = await db.master_resume_collection.find_one(
        {"user_id": ObjectId(user["_id"])}
    )

    if not resume:
        raise HTTPException(404, "Profile not initialized")

    old_key = resume.get("profilePicture")

    if old_key:
        try:
            await delete_object(old_key)
        except Exception:
            pass

    key = await upload_profile_picture(file)

    await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$set": {"profilePicture": key}}
    )

    signed_url = await generate_signed_url(key)

    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Profile Picture updated",
        "data": {"signed_url": signed_url}
    }

@router.delete("/image")
async def delete_picture(user=Depends(get_current_user)):

    db = get_database()
    redis_client = get_redis()

    resume = await db.master_resume_collection.find_one(
        {"user_id": ObjectId(user["_id"])}
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    prof_pic_key = resume.get("profilePicture")

    if prof_pic_key:
        try:
            await delete_object(prof_pic_key)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete image from S3: {str(e)}"
            )

    await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$set": {"profilePicture": None}}
    )

    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Profile Picture Deleted",
        "data": {"signed_url": None}
    }

@router.patch("/image/toggle-visibility")
async def toggle_image_visibility(user=Depends(get_current_user)):
    db = get_database()
    redis_client = get_redis()

    result = await db.master_resume_collection.find_one_and_update(
        {"user_id": ObjectId(user["_id"])},
        [
            {
                "$set": {
                    "hideProfilePicture": {
                        "$not": ["$hideProfilePicture"]
                    }
                }
            }
        ],
        return_document=True
    )

    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Updated Profile Images Visibility",
        "data": {
            "hideProfilePicture": result["hideProfilePicture"]
        }
    }

@router.patch("/declaration")
async def update_declaration(
    data: profile_schema.DeclarationUpdate,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()
    query = get_top_level_update_query("declaration", data)

    result = await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        query
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Profile not initialized")
    
    await redis_client.delete(f"profile:{user['_id']}")

    dump_model = data.model_dump(exclude_unset=True)

    return {
        "success": True,
        "message": "Declaration updated",
        "data": jsonable_encoder(dump_model)
    }

@router.patch("/declaration/signature")
async def upload_signature(file: UploadFile = File(...), user=Depends(get_current_user)):

    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(400, "Only PNG/JPG allowed")
    
    if file.size > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    
    db = get_database()
    redis_client = get_redis()

    resume = await db.master_resume_collection.find_one(
        {"user_id": ObjectId(user["_id"])}
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    declaration = resume.get("declaration", {})
    signature_key = declaration.get("signature")

    if signature_key:
        try:
            await delete_object(signature_key)
        except Exception:
            pass

    key = await upload_signature_s3(file)

    await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$set": {"declaration.signature": key}}
    )

    signed_url = await generate_signed_url(key)

    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Declaration Signature updated",
        "data": {"signed_url": signed_url}
    }

@router.delete("/declaration/signature")
async def delete_signature(user=Depends(get_current_user)):

    db = get_database()
    redis_client = get_redis()

    resume = await db.master_resume_collection.find_one(
        {"user_id": ObjectId(user["_id"])}
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Profile not initialized"
        )
    
    declaration = resume.get("declaration", {})
    signature_key = declaration.get("signature")

    if signature_key:
        try:
            await delete_object(signature_key)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete image from S3: {str(e)}"
            )

    await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        {"$set": {"declaration.signature": None}}
    )

    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Declaration Signature Deleted",
        "data": {"signed_url": None}
    }

@router.patch("/summary")
async def update_summary(
    data: profile_schema.ProfileSummarySchema,
    user=Depends(get_current_user)
):
    db = get_database()
    redis_client = get_redis()

    query = get_update_query(data)

    await db.master_resume_collection.update_one(
        {"user_id": ObjectId(user["_id"])},
        query
    )

    await redis_client.delete(f"profile:{user['_id']}")

    return {
        "success": True,
        "message": "Profile Summary updated",
        "data": jsonable_encoder(data)
    }


@router.patch("/onboarding")
async def complete_onboarding(user=Depends(get_current_user)):
    db = get_database()

    await db.users_collection.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {
            "onboarding_complete": True
        }}
    )

    return {
        "success": True,
        "message": "Onboarding Complete",
        "data": {"onboarding_complete": True}
    }