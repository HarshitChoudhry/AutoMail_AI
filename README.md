# AutoMail_AI
AI-powered email generation

## 📌 Project Overview

This tool helps job seekers generate personalized cold emails when applying for jobs. It:

Extracts job details from a given job listing webpage.

Parses and analyzes your resume to extract relevant skills.

Generates a customized email based on your skills and the job description.

Built with LangChain, ChromaDB, Streamlit, and NLP techniques, this tool automates email writing for job applications.

## ✨ Features

Scrape Job Listings: Extracts job details from a webpage.

Resume Parsing: Extracts and analyzes skills from PDF/DOCX resumes.

AI-Powered Email Generation: Creates a customized cold email.

Interactive UI: Simple Streamlit-based web app.

## 🛠 Installation

1️⃣ Clone the Repository

git clone https://github.com/your-repo/job-email-generator.git
cd job-email-generator

2️⃣ Create and Activate a Virtual Environment

## For Windows
python -m venv venv
venv\Scripts\activate

## For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file and add your GROQ API Key:

GROQ_API_KEY=your_api_key_here

## 🚀 Usage

Run the Streamlit app using:

streamlit run main.py

How to Use:

Enter Job Listing URL

Upload Resume (PDF/DOCX)

Click 'Generate Email'

Copy & Use the Personalized Email!

## ⚙️ How It Works

Job Extraction (chains.py):

Scrapes job details using LangChain.

Extracts role, experience, skills, and description.

Resume Parsing (portfolio.py & utils.py):

Reads PDF/DOCX resumes and extracts skills.

Uses predefined skill keywords for matching.

Stores extracted skills in ChromaDB.

Email Generation (chains.py):

Uses extracted job details + resume skills.

Generates a custom cold email using LLM.

## 🏗 Tech Stack

Python

Streamlit (Web UI)

LangChain (LLM Processing)

ChromaDB (Vector Storage)

pdfplumber / docx2txt (Resume Parsing)

GROQ API (LLM Backend)

