# Job Posting & Application System

## Database Models

### 1. **Job Model** (`jobs` table)
Stores job postings created by recruiters.

**Fields:**
- `id` - Primary key
- `recruiter_id` - Foreign key to users (who posted the job)
- `job_title` - e.g., "Senior Python Developer"
- `company_name` - e.g., "Tech Corp Inc"
- `job_description` - Full job description (Text field)
- `skills` - Comma-separated skills (e.g., "Python, React, SQL")
- `location` - e.g., "New York, NY" or "Remote"
- `salary_range` - e.g., "$80k - $120k"
- `employment_type` - "Full-time", "Part-time", "Contract", etc.
- `experience_level` - "Entry", "Mid", "Senior"
- `is_active` - Boolean (can close/archive jobs)
- `created_at` - Timestamp
- `updated_at` - Timestamp

**Relationships:**
- Belongs to one `User` (recruiter)
- Has many `Application` records

---

### 2. **Application Model** (`applications` table)
Tracks applications submitted by applicants for specific jobs.

**Fields:**
- `id` - Primary key
- `job_id` - Foreign key to jobs
- `applicant_id` - Foreign key to users (applicant)
- `resume_id` - Foreign key to resumes (which resume they used)
- `status` - "pending", "reviewed", "accepted", "rejected"
- `applied_at` - Timestamp

**Relationships:**
- Belongs to one `Job`
- Belongs to one `User` (applicant)
- Belongs to one `Resume`

---

## Use Cases

### For Applicants:
1. **View Job Listings** - Browse available jobs on their dashboard
2. **View Job Details** - See full job description, skills required
3. **Apply to Jobs** - Select a resume and apply to a job
4. **Track Applications** - See status of their applications

### For Recruiters:
1. **Post Jobs** - Create new job postings
2. **View All Jobs** - See all their posted jobs with application counts
3. **View Applications** - See all applicants for a specific job
4. **View Applicant Resumes** - Access resume details and scores
5. **Manage Job Status** - Activate/deactivate job postings

---

## API Endpoints Needed

### Job Endpoints (for Recruiters):
- `POST /jobs` - Create new job posting
- `GET /jobs/my-jobs` - Get all jobs posted by recruiter
- `GET /jobs/{job_id}` - Get specific job details
- `PUT /jobs/{job_id}` - Update job posting
- `DELETE /jobs/{job_id}` - Delete job posting
- `GET /jobs/{job_id}/applications` - Get all applications for a job

### Job Endpoints (for Applicants):
- `GET /jobs` - Get all active job postings
- `GET /jobs/{job_id}` - Get specific job details
- `GET /jobs/applied` - Get jobs applicant has applied to

### Application Endpoints:
- `POST /applications` - Apply to a job (applicants)
- `GET /applications/my-applications` - Get applicant's applications
- `PUT /applications/{app_id}/status` - Update application status (recruiters)

---

## Frontend Views

### Applicant Dashboard:
- **Jobs Section**: Display job cards with:
  - Job title and company
  - Skills (as chips)
  - Location, salary, employment type
  - "Apply" button
- **My Applications**: List of jobs applied to with status

### Recruiter Dashboard:
- **Job Overview**: Summary card showing:
  - Total jobs posted
  - Total applications received
  - Active jobs count
- **My Jobs**: List of all posted jobs with:
  - Job title
  - Application count
  - Status (active/inactive)
  - "View Applications" button
- **Applications by Job**: Detailed view showing all applicants for a specific job

---

## Data Flow

1. **Recruiter posts job** → Job saved to `jobs` table
2. **Applicant views jobs** → API returns active jobs
3. **Applicant applies** → Application saved to `applications` table
4. **Recruiter views applications** → API returns applications with resume details
5. **Recruiter updates status** → Application status updated in database
