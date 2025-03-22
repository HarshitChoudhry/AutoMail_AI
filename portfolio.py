import pandas as pd
import chromadb
import uuid
import fitz
import docx2txt
from utils import clean_text  # ✅ Import clean_text function

class Portfolio:
    def __init__(self):
        # Initialize ChromaDB for storing resume-based data
        self.chroma_client = chromadb.PersistentClient("vectorstore_personal")
        self.collection = self.chroma_client.get_or_create_collection(name="personal_resume")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        doc = fitz.open(pdf_path)
        text = " ".join([page.get_text("text") for page in doc])
        return text
    
    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file."""
        return docx2txt.process(docx_path)
    
    def extract_skills_from_resume(self, resume_text):
        """Extract skills from resume text using predefined keywords."""
        skill_keywords = [
            "Python", "Machine Learning", "Deep Learning", "Data Science", "NLP",
            "Computer Vision", "SQL", "TensorFlow", "PyTorch", "Pandas", "NumPy",
            "Excel", "Power BI", "AWS", "Docker", "MLOps", "JavaScript", "React"
        ]
        extracted_skills = [skill for skill in skill_keywords if skill.lower() in resume_text.lower()]
        return extracted_skills
    
    def load_resume(self, file_path):
        """Load the resume, extract skills, and store in ChromaDB."""
        if file_path.endswith(".pdf"):
            resume_text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            resume_text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Upload a PDF or DOCX.")

        cleaned_resume_text = clean_text(resume_text)  # ✅ Use imported clean_text function
        skills = self.extract_skills_from_resume(cleaned_resume_text)

        # Convert list to a comma-separated string ✅
        skills_str = ", ".join(skills)  

        # Store extracted skills in ChromaDB
        if self.collection.count() == 0:  # Ensure no duplicate entries
            self.collection.add(
                documents=[skills_str],  # ✅ Store skills as a single string
                metadatas={"skills": skills_str},  # ✅ ChromaDB requires metadata values to be str, int, float, or bool
                ids=[str(uuid.uuid4())]
            )
