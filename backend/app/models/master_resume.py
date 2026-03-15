from typing import List, Optional
from app.models.base import MongoBaseModel, PyObjectId
from app.schemas import profile_schema
from pydantic import Field

class MasterResume(MongoBaseModel):
    user_id: PyObjectId
    personalDetails: profile_schema.PersonalDetails
    profileSummary: Optional[str] = None
    hideProfileSummary: bool = Field(default=False, description="Toggle to hide the summary on the generated PDF/Web view")
    profilePicture: Optional[str] = None
    hideProfilePicture: bool = Field(default=False, description="Toggle to hide the photo on the generated PDF/Web view")
    educationDetails: List[profile_schema.EducationResponse] = []
    professionalExperiences: List[profile_schema.ProfessionalExpResponse] = []
    skills: List[profile_schema.SkillResponse] = []
    languages: List[profile_schema.LanguageResponse] = []
    certificates: Optional[List[profile_schema.CertificateResponse]] = []
    projects: List[profile_schema.ProjectResponse] = []
    awards: List[profile_schema.AwardResponse] = []
    courses: List[profile_schema.CourseResponse] = []
    organizations: List[profile_schema.OrganizationResponse] = []
    publications: List[profile_schema.PublicationResponse] = []
    references: List[profile_schema.ReferenceResponse] = []
    declaration: profile_schema.DeclarationSchema = {}