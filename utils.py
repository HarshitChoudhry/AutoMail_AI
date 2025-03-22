import re
import docx2txt
import pdfplumber

# Predefined list of skills to match against (Can be expanded)
SKILL_SET = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning", "NLP", "Data Science", 
    "SQL", "TensorFlow", "PyTorch", "AWS", "Azure", "Google Cloud", "Power BI", "Tableau",
    "Docker", "MLOps", "Flask", "Git","GenAI"
]

def clean_text(text):
    """Clean raw text by removing unwanted characters, links, and excessive whitespace."""
    text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML tags
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Remove special characters
    text = re.sub(r'\s{2,}', ' ', text).strip()  # Remove extra spaces
    return text

def extract_resume_skills(resume_file):
    """Extracts skills from a PDF or DOCX resume."""
    text = ""
    
    if resume_file.type == "application/pdf":
        with pdfplumber.open(resume_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    
    elif resume_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        text = docx2txt.process(resume_file)

    text = clean_text(text).lower()
    
    # Extract matching skills
    extracted_skills = [skill for skill in SKILL_SET if skill.lower() in text]
    
    return extracted_skills if extracted_skills else ["No matching skills found"]
