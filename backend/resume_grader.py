import re
import PyPDF2
from typing import Dict
from io import BytesIO


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def grade_resume(file_path: str, file_content: bytes) -> Dict:
    """
    Grade a resume based on multiple criteria
    Returns a dictionary with scores and feedback
    """
    
    # Extract text from resume
    text = ""
    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_content)
    else:
        # For .doc/.docx, you'd need python-docx library
        # For now, we'll use a placeholder
        text = "Document text extraction requires additional processing"
    
    text_lower = text.lower()
    
    # Initialize scores
    scores = {
        "formatting_score": 0,
        "content_score": 0,
        "keyword_score": 0,
        "experience_score": 0,
        "education_score": 0,
    }
    
    feedback_items = []
    
    # 1. Formatting Score (0-20 points)
    formatting_score = 0
    if len(text) > 200:
        formatting_score += 5
        feedback_items.append("✓ Good document length")
    else:
        feedback_items.append("✗ Resume seems too short")
    
    # Check for structure indicators
    sections = ['experience', 'education', 'skills', 'summary', 'objective']
    found_sections = sum(1 for section in sections if section in text_lower)
    formatting_score += min(found_sections * 3, 15)
    if found_sections >= 3:
        feedback_items.append(f"✓ Well-structured with {found_sections} key sections")
    else:
        feedback_items.append("✗ Missing important sections (experience, education, skills)")
    
    scores["formatting_score"] = formatting_score
    
    # 2. Content Score (0-20 points)
    content_score = 0
    
    # Check for contact information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    if re.search(email_pattern, text):
        content_score += 5
        feedback_items.append("✓ Email address found")
    else:
        feedback_items.append("✗ No email address found")
    
    if re.search(phone_pattern, text):
        content_score += 5
        feedback_items.append("✓ Phone number found")
    
    # Check for action verbs
    action_verbs = ['developed', 'managed', 'created', 'led', 'implemented', 
                    'designed', 'achieved', 'improved', 'increased', 'reduced']
    action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    content_score += min(action_verb_count * 2, 10)
    if action_verb_count >= 3:
        feedback_items.append(f"✓ Good use of action verbs ({action_verb_count} found)")
    else:
        feedback_items.append("✗ Limited use of action verbs - use more impactful language")
    
    scores["content_score"] = content_score
    
    # 3. Keyword Score (0-20 points)
    keyword_score = 0
    
    # Technical keywords
    technical_keywords = ['python', 'javascript', 'java', 'react', 'vue', 'angular',
                         'node', 'sql', 'aws', 'azure', 'docker', 'kubernetes',
                         'agile', 'scrum', 'git', 'api', 'database', 'frontend',
                         'backend', 'full stack', 'machine learning', 'ai']
    
    found_keywords = [kw for kw in technical_keywords if kw in text_lower]
    keyword_score = min(len(found_keywords) * 2, 20)
    
    if len(found_keywords) >= 5:
        feedback_items.append(f"✓ Strong technical keywords ({len(found_keywords)} found)")
    elif len(found_keywords) >= 2:
        feedback_items.append(f"⚠ Moderate technical keywords ({len(found_keywords)} found)")
    else:
        feedback_items.append("✗ Lacks relevant technical keywords")
    
    scores["keyword_score"] = keyword_score
    
    # 4. Experience Score (0-20 points)
    experience_score = 0
    
    # Look for date patterns indicating work experience
    date_patterns = [
        r'\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}\b',  # 2020-2023
        r'\b(19|20)\d{2}\s*[-–]\s*present\b',        # 2020-present
        r'\b\w+\s+(19|20)\d{2}\s*[-–]\s*\w+\s+(19|20)\d{2}\b'  # Jan 2020 - Dec 2023
    ]
    
    date_matches = 0
    for pattern in date_patterns:
        date_matches += len(re.findall(pattern, text_lower))
    
    experience_score = min(date_matches * 5, 15)
    
    # Check for experience-related terms
    if 'years of experience' in text_lower or 'year of experience' in text_lower:
        experience_score += 5
    
    if experience_score >= 15:
        feedback_items.append("✓ Detailed work experience with dates")
    elif experience_score >= 8:
        feedback_items.append("⚠ Some work experience mentioned")
    else:
        feedback_items.append("✗ Work experience not clearly documented")
    
    scores["experience_score"] = experience_score
    
    # 5. Education Score (0-20 points)
    education_score = 0
    
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university',
                         'college', 'diploma', 'certification', 'certificate']
    
    found_education = [kw for kw in education_keywords if kw in text_lower]
    education_score = min(len(found_education) * 5, 15)
    
    # Check for GPA mention
    if re.search(r'\bgpa\b|\b[3-4]\.\d+\b', text_lower):
        education_score += 5
        feedback_items.append("✓ Academic performance mentioned")
    
    if education_score >= 15:
        feedback_items.append("✓ Strong educational background")
    elif education_score >= 8:
        feedback_items.append("⚠ Education section present")
    else:
        feedback_items.append("✗ Education details unclear or missing")
    
    scores["education_score"] = education_score
    
    # Calculate overall score
    overall_score = sum(scores.values())
    
    # Generate overall feedback
    if overall_score >= 80:
        overall_feedback = "Excellent resume! Strong across all categories."
    elif overall_score >= 60:
        overall_feedback = "Good resume with room for minor improvements."
    elif overall_score >= 40:
        overall_feedback = "Decent resume but needs significant improvements."
    else:
        overall_feedback = "Resume needs major revisions to be competitive."
    
    feedback_items.insert(0, f"Overall Assessment: {overall_feedback}")
    
    return {
        "overall_score": overall_score,
        "formatting_score": scores["formatting_score"],
        "content_score": scores["content_score"],
        "keyword_score": scores["keyword_score"],
        "experience_score": scores["experience_score"],
        "education_score": scores["education_score"],
        "feedback": "\n".join(feedback_items),
        "extracted_text": text[:500] + "..." if len(text) > 500 else text
    }


