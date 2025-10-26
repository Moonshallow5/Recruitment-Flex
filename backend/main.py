from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from config import settings
from database import get_db, engine
from models import Base, User, Resume, Job, Application
from schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    ResumeResponse,
    JobCreate, JobUpdate, JobResponse, JobListResponse,
    ApplicationCreate, ApplicationResponse, ApplicationDetailResponse
)
from auth import create_access_token, get_current_user, get_password_hash, verify_password
from resume_grader import grade_resume
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recruitment API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory (already done in config.py, but keep for safety)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for serving resumes
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def read_root():
    return {"message": "Recruitment API is running"}


# Authentication endpoints
@app.post("/auth/register", response_model=dict)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}


@app.post("/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "name": user.name,
        "role": user.role
    }


@app.get("/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


# Resume endpoints
@app.post("/resumes/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user is applicant
    if current_user.role != "applicant":
        raise HTTPException(status_code=403, detail="Only applicants can upload resumes")
    
    # Validate file type
    allowed_extensions = [".pdf", ".doc", ".docx"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = f"uploads/resumes/{current_user.id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Grade resume
    grading_result = grade_resume(file_path, content)
    
    # Save to database
    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        file_size=len(content),
        overall_score=grading_result["overall_score"],
        formatting_score=grading_result["formatting_score"],
        content_score=grading_result["content_score"],
        keyword_score=grading_result["keyword_score"],
        experience_score=grading_result["experience_score"],
        education_score=grading_result["education_score"],
        feedback=grading_result["feedback"],
        extracted_text=grading_result.get("extracted_text", "")
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return resume


@app.get("/resumes/my-resumes", response_model=List[ResumeResponse])
def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "applicant":
        raise HTTPException(status_code=403, detail="Only applicants can view their resumes")
    
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes


@app.get("/resumes/all", response_model=List[dict])
def get_all_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can view all resumes")
    
    resumes = db.query(Resume).join(User).all()
    
    # Format response with user information
    result = []
    for resume in resumes:
        # Find if this resume is linked to any job application
        # for jobs posted by this recruiter
        application = db.query(Application).join(Job).filter(
            Application.resume_id == resume.id,
            Job.recruiter_id == current_user.id
        ).first()
        
        resume_data = {
            "id": resume.id,
            "filename": resume.filename,
            "uploaded_at": resume.uploaded_at,
            "overall_score": resume.overall_score,
            "formatting_score": resume.formatting_score,
            "content_score": resume.content_score,
            "keyword_score": resume.keyword_score,
            "experience_score": resume.experience_score,
            "education_score": resume.education_score,
            "feedback": resume.feedback,
            "applicant_name": resume.user.name,
            "applicant_email": resume.user.email,
            "applicant_id": resume.user_id,
            "job_id": application.job_id if application else None
        }
        result.append(resume_data)
    
    return result


@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check permissions
    if current_user.role == "applicant" and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view your own resumes")
    
    return resume


# Job endpoints
@app.post("/jobs", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403, detail="Only recruiters can create jobs"
        )
    
    new_job = Job(
        recruiter_id=current_user.id,
        **job_data.model_dump()
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@app.get("/jobs", response_model=List[JobResponse])
def get_active_jobs(
    db: Session = Depends(get_db)
):
    """Get all active jobs (for applicants)"""
    jobs = db.query(Job).filter(Job.is_active.is_(True)).all()
    return jobs


@app.get("/jobs/my-jobs", response_model=List[JobListResponse])
def get_my_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403, detail="Only recruiters can view their jobs"
        )
    
    jobs = db.query(Job).filter(Job.recruiter_id == current_user.id).all()
    
    # Format response with application count
    result = []
    for job in jobs:
        app_count = db.query(Application).filter(
            Application.job_id == job.id
        ).count()
        
        result.append({
            **{col: getattr(job, col) for col in job.__table__.columns.keys()},
            "applications_count": app_count
        })
    
    return result


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403, detail="Only recruiters can update jobs"
        )
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own jobs"
        )
    
    # Update fields
    update_data = job_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
    
    db.commit()
    db.refresh(job)
    return job


@app.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403, detail="Only recruiters can delete jobs"
        )
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only delete your own jobs"
        )
    
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}


@app.get("/jobs/{job_id}/applications", response_model=List[ApplicationDetailResponse])
def get_job_applications(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(
            status_code=403, detail="Only recruiters can view applications"
        )
    
    # Verify job belongs to recruiter
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only view applications for your own jobs"
        )
    
    applications = db.query(Application).filter(Application.job_id == job_id).all()
    
    # Format response with user and resume details
    result = []
    for app in applications:
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "applicant_id": app.applicant_id,
            "resume_id": app.resume_id,
            "status": app.status,
            "applied_at": app.applied_at,
            "applicant_name": app.applicant.name,
            "applicant_email": app.applicant.email,
            "resume_filename": app.resume.filename,
            "resume_score": app.resume.overall_score
        })
    
    return result


# Application endpoints
@app.post("/applications", response_model=ApplicationResponse)
def apply_to_job(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "applicant":
        raise HTTPException(
            status_code=403, detail="Only applicants can apply to jobs"
        )
    
    # Check if already applied
    existing = db.query(Application).filter(
        Application.job_id == application_data.job_id,
        Application.applicant_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, detail="You have already applied to this job"
        )
    
    # Verify resume belongs to user
    resume = db.query(Resume).filter(Resume.id == application_data.resume_id).first()
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Verify job exists and is active
    job = db.query(Job).filter(Job.id == application_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job.is_active:
        raise HTTPException(status_code=400, detail="This job is no longer active")
    
    new_application = Application(
        job_id=application_data.job_id,
        applicant_id=current_user.id,
        resume_id=application_data.resume_id,
        status="pending"
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


@app.get("/applications/my-applications", response_model=List[dict])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "applicant":
        raise HTTPException(
            status_code=403, detail="Only applicants can view their applications"
        )
    
    applications = db.query(Application).filter(
        Application.applicant_id == current_user.id
    ).all()
    
    # Build response with job and resume details
    result = []
    for app in applications:
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "applicant_id": app.applicant_id,
            "resume_id": app.resume_id,
            "status": app.status,
            "applied_at": app.applied_at,
            "resume": {
                "id": app.resume.id,
                "filename": app.resume.filename,
                "file_path": app.resume.file_path,
                "file_size": app.resume.file_size,
                "overall_score": app.resume.overall_score,
                "formatting_score": app.resume.formatting_score,
                "content_score": app.resume.content_score,
                "keyword_score": app.resume.keyword_score,
                "experience_score": app.resume.experience_score,
                "education_score": app.resume.education_score,
                "feedback": app.resume.feedback,
                "uploaded_at": app.resume.uploaded_at
            },
            "job": {
                "id": app.job.id,
                "job_title": app.job.job_title,
                "company_name": app.job.company_name,
                "job_description": app.job.job_description,
                "skills": app.job.skills,
                "location": app.job.location,
                "salary_range": app.job.salary_range,
                "employment_type": app.job.employment_type,
                "experience_level": app.job.experience_level,
                "is_active": app.job.is_active,
                "created_at": app.job.created_at,
                "updated_at": app.job.updated_at
            }
        })
    
    return result


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


