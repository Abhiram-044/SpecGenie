from pydantic import EmailStr, Field, BaseModel, HttpUrl
from typing import List, Optional, Literal
from app.models.base import PyObjectId
from datetime import date

class SocialLink(BaseModel):
    platform: Literal[
        "Linkedin",
        "Github",
        "Twitter",
        "Youtube",
        "Dribbble",
        "Behance",
        "Stackoverflow",
        "Website"
    ]
    url: HttpUrl
    link: str

class PersonalDetails(BaseModel):
    fullName: Optional[str] = None
    jobTitle: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    personalInfo: Optional[str] = None
    dateOfBirth: Optional[date] = None
    nationality: Optional[str] = None
    passport_govt_id: Optional[str] = None
    maritialStatus: Optional[
        Literal["Single", "Married", "Divorced", "Separated", "Partnered", "Prefer Not to Say"]
    ] = None
    militaryStatus: Optional[
        Literal["Currently Serving", "Veteran", "Reserved"]
    ] = None
    drivingLicense: Optional[str] = None
    genderPronouns: Optional[
        Literal["He / Him", "She / Her", "They / Them", "Preferred Not to Say"]
    ] = None
    visa: Optional[str] = None
    socialLinks: List[SocialLink] = []

class EducationCreate(BaseModel):
    degree: str
    school: str
    grade: Optional[str] = None
    link: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    description: Optional[str] = None
    hide: bool = False

class EducationResponse(EducationCreate):
    id: PyObjectId = Field(alias="_id")

class ProfessionalExpCreate(BaseModel):
    jobTitle: str
    employer: str
    link: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    description: Optional[str] = None
    hide: bool = False

class ProfessionalExpResponse(ProfessionalExpCreate):
    id: PyObjectId = Field(alias="_id")

class SkillCreate(BaseModel):
    name: str
    subSkils: List[str] = []
    level: Optional[
        Literal["BEGINNER", "AMATEUR", "COMPETENT", "PROFICIENT", "EXPERT"]
    ] = None
    hide: bool = False

class SkillResponse(SkillCreate):
    id: PyObjectId = Field(alias="_id")

class LanguageCreate(BaseModel):
    name: str
    additionalInfo: Optional[str] = None
    level: Optional[
        Literal["BASIC", "CONVERSATIONAL", "PROFICIENT", "FLUENT", "NATIVE"]
    ] = None
    hide: bool = False

class LanguageResponse(LanguageCreate):
    id: PyObjectId = Field(alias="_id")

class CertificateCreate(BaseModel):
    title: str
    link: Optional[str] = None
    license: Optional[str] = None
    issuer: Optional[str] = None
    issueDate: Optional[date] = None
    expirationDate: Optional[date] = None
    additionalInfo: Optional[str] = None
    hide: bool = False

class CertificateResponse(CertificateCreate):
    id: PyObjectId = Field(alias="_id")

class ProjectLinks(BaseModel):
    url: HttpUrl
    platform: Literal["GITHUB", "WEBSITE", "PLAY_STORE", "APP_STORE", "OTHER"]

class ProjectCreate(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    links: Optional[List[ProjectLinks]] = []
    hide: bool = False

class ProjectResponse(ProjectCreate):
    id: PyObjectId = Field(alias="_id")

class AwardCreate(BaseModel):
    title: str
    issuer: Optional[str] = None
    issueDate: Optional[date] = None
    hide: bool = False

class AwardResponse(AwardCreate):
    id: PyObjectId = Field(alias="_id")

class CourseCreate(BaseModel):
    title: str
    license: Optional[str] = None
    issuer: Optional[str] = None
    issueDate: Optional[date] = None
    expirationDate: Optional[date] = None
    additionalInfo: Optional[str] = None
    hide: bool = False

class CourseResponse(CourseCreate):
    id: PyObjectId = Field(alias="_id")

class OrganizationCreate(BaseModel):
    name: str
    link: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    description: Optional[str] = None
    hide: bool = False

class OrganizationResponse(OrganizationCreate):
    id: PyObjectId = Field(alias="_id")

class PublicationCreate(BaseModel):
    title: str
    link: Optional[str] = None
    publisher: Optional[str] = None
    issueDate: Optional[date] = None
    description: Optional[str] = None
    hide: bool = False

class PublicationResponse(PublicationCreate):
    id: PyObjectId = Field(alias="_id")

class ReferenceCreate(BaseModel):
    name: str
    link: Optional[str] = None
    jobTitle: Optional[str] = None
    organization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    hide: bool = False

class ReferenceResponse(ReferenceCreate):
    id: PyObjectId = Field(alias="_id")

class DeclarationSchema(BaseModel):
    text: Optional[str] = None
    fullName: Optional[str] = None
    signature: Optional[str] = None
    place: Optional[str] = None
    issueDate: Optional[date] = None
    hide: bool = False

class ProfileSummarySchema(BaseModel):
    profileSummary: Optional[str] = None
    hideProfileSummary: Optional[bool] = None