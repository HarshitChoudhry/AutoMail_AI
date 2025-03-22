import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from utils import extract_resume_skills

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant"
        )

    def extract_jobs(self, cleaned_text):
        """Extracts job details from a given job posting webpage text."""
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            
            ### INSTRUCTION:
            The scraped text is from a job listing webpage. Extract and return job details in JSON format
            with these keys: `role`, `experience`, `skills`, and `description`.
            Ensure the response is a valid JSON.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, resume_file):
        """Generate a personalized cold email based on the user's resume and job description."""
        resume_skills = extract_resume_skills(resume_file)
        
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### CANDIDATE PROFILE:
            Skills extracted from the candidate's resume: {resume_skills}
            
            ### INSTRUCTION:
            You are an individual job seeker applying for the above job. 
            Your task is to write a personalized cold email expressing interest in the job, 
            highlighting the candidate's relevant skills and experience. Keep the email concise and professional.
            
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "resume_skills": ", ".join(resume_skills)
        })
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))