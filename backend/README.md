# Recruitment API Backend

FastAPI backend for the recruitment platform with resume upload and grading functionality.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Authentication
- `POST /auth/register` - Register new user (applicant or recruiter)
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Resumes
- `POST /resumes/upload` - Upload resume (applicant only)
- `GET /resumes/my-resumes` - Get all resumes for current applicant
- `GET /resumes/all` - Get all resumes with grades (recruiter only)
- `GET /resumes/{resume_id}` - Get specific resume details

## Resume Grading System

The system automatically grades resumes on:
- **Formatting (20 points)**: Document structure and organization
- **Content (20 points)**: Contact info, action verbs, and writing quality
- **Keywords (20 points)**: Relevant technical and industry keywords
- **Experience (20 points)**: Work history documentation
- **Education (20 points)**: Educational background and achievements

**Total Score: 0-100 points**

## Database

Uses SQLite by default. Database file: `recruitment.db`

To switch to PostgreSQL or MySQL, update `database.py` with appropriate connection string.

## Security

⚠️ **Important**: Change the `SECRET_KEY` in `auth.py` before deploying to production!


