import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio):
    """Creates the Streamlit UI for generating personalized job application emails."""
    st.title("📧 Personalized Job Application Email Generator")

    # User Inputs
    url_input = st.text_input("Enter the Job Listing URL:")
    resume_file = st.file_uploader("Upload Your Resume (PDF or DOCX) (Max: 10MB)", type=["pdf", "docx"])
    submit_button = st.button("Generate Email")

    if submit_button:
        if not resume_file:
            st.error("⚠️ Please upload your resume before generating an email.")
            return

        # Check file size (convert bytes to MB)
        resume_file.seek(0, 2)  # Move pointer to end of file
        file_size_mb = resume_file.tell() / (1024 * 1024)  # Convert bytes to MB
        resume_file.seek(0)  # Reset pointer to start

        if file_size_mb > 10:
            st.error("❌ File size exceeds 10MB. Please upload a smaller file.")
            return

        try:
            # Extract text & skills from resume
            resume_path = f"./temp_resume.{resume_file.name.split('.')[-1]}"  # Temporary file path
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            portfolio.load_resume(resume_path)
            skills = portfolio.collection.get(include=["metadatas"])["metadatas"][0]["skills"]

            # Load job details
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)

            # Generate email for each job
            for job in jobs:
                email = llm.write_mail(job, resume_file)
                st.subheader(f"📩 Personalized Email for {job['role']}")
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"❌ An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Personalized Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio)
