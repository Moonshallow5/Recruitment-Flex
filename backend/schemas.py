from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    role: str  # 'applicant' or 'recruiter'


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    name: str
    role: str


class ResumeUpload(BaseModel):
    filename: str


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_size: int
    overall_score: float
    formatting_score: float
    content_score: float
    keyword_score: float
    experience_score: float
    education_score: float
    feedback: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class ResumeGradeResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    overall_score: float
    formatting_score: float
    content_score: float
    keyword_score: float
    experience_score: float
    education_score: float
    feedback: str
    applicant_name: str
    applicant_email: str
    applicant_id: int


# Job posting schemas
class JobCreate(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    skills: str  # Comma-separated
    location: Optional[str] = None
    salary_range: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None


class JobUpdate(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    job_description: Optional[str] = None
    skills: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    is_active: Optional[bool] = None


class JobResponse(BaseModel):
    id: int
    recruiter_id: int
    job_title: str
    company_name: str
    job_description: str
    skills: str
    location: Optional[str]
    salary_range: Optional[str]
    employment_type: Optional[str]
    experience_level: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    id: int
    job_title: str
    company_name: str
    job_description: str
    skills: str
    location: Optional[str]
    salary_range: Optional[str]
    employment_type: Optional[str]
    experience_level: Optional[str]
    is_active: bool
    created_at: datetime
    applications_count: int = 0  # Count of applications
    
    class Config:
        from_attributes = True


# Application schemas
class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: int


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    resume_id: int
    status: str
    applied_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationDetailResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    resume_id: int
    status: str
    applied_at: datetime
    # Expanded fields
    applicant_name: str
    applicant_email: str
    resume_filename: str
    resume_score: float
    
    class Config:
        from_attributes = True


class MyApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    resume_id: int
    status: str
    applied_at: datetime
    # Resume details
    resume: Optional[ResumeResponse] = None
    # Job details
    job: Optional[JobResponse] = None
    
    class Config:
        from_attributes = True


