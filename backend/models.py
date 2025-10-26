from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'applicant' or 'recruiter'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resumes = relationship("Resume", back_populates="user")
    jobs = relationship("Job", back_populates="recruiter")
    applications = relationship("Application", back_populates="applicant")


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    
    # Grading scores
    overall_score = Column(Float)
    formatting_score = Column(Float)
    content_score = Column(Float)
    keyword_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    
    feedback = Column(Text)
    extracted_text = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Link to recruiter who posted the job
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    job_description = Column(Text, nullable=False)
    skills = Column(String, nullable=False)  # Comma-separated skills
    location = Column(String)
    salary_range = Column(String)  # e.g., "$50k - $80k"
    employment_type = Column(
        String
    )  # e.g., "Full-time", "Part-time", "Contract"
    experience_level = Column(String)  # "Entry", "Mid", "Senior"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    recruiter = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    status = Column(
        String, default="pending"
    )  # pending, reviewed, accepted, rejected
    applied_at = Column(DateTime, default=datetime.utcnow)
    
    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")


