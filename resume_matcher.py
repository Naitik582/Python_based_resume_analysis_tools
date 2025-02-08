import os
import pandas as pd
import re
import docx2txt
from pdfminer.high_level import extract_text

# Predefined skills list (Modify as per requirement)
skills_list = [
    "Python", "SQL", "Excel", "Power BI", "Machine Learning", "Tableau", 
    "Data Science", "Statistics", "Deep Learning", "Artificial Intelligence",
    "NLP", "Pandas", "NumPy", "Scikit-learn", "Matplotlib", "TensorFlow"
]

# Function to extract text from PDF resume
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Function to extract text from DOCX resume
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Function to extract skills from text
def extract_skills(text, skills_list):
    text = text.lower()
    extracted_skills = [skill for skill in skills_list if skill.lower() in text]
    return extracted_skills

# Function to calculate skill match percentage
def calculate_match(resume_skills, jd_skills):
    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)
    match_percentage = (len(matched) / len(jd_skills) * 100) if jd_skills else 0
    return match_percentage, matched, missing

# Function to process resume and job description
def process_resume(resume_path, job_description_path):
    # Extract resume text
    if resume_path.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith(".docx"):
        resume_text = extract_text_from_docx(resume_path)
    else:
        print("Unsupported file format!")
        return
    
    # Extract job description text
    with open(job_description_path, "r", encoding="utf-8") as file:
        job_description_text = file.read().lower()
    
    # Extract skills from resume and job description
    resume_skills = extract_skills(resume_text, skills_list)
    jd_skills = extract_skills(job_description_text, skills_list)

    # Calculate matching percentage
    match_percentage, matched_skills, missing_skills = calculate_match(resume_skills, jd_skills)

    # Print results
    print("\n--- Resume Analysis Report ---")
    print(f"Match Percentage: {match_percentage:.2f}%")
    print("Matched Skills:", ", ".join(matched_skills))
    print("Missing Skills:", ", ".join(missing_skills))
    
    # Save results to CSV
    result_data = {
        "Resume Skills": [", ".join(resume_skills)],
        "Job Description Skills": [", ".join(jd_skills)],
        "Matched Skills": [", ".join(matched_skills)],
        "Missing Skills": [", ".join(missing_skills)],
        "Match Percentage": [match_percentage]
    }
    
    df = pd.DataFrame(result_data)
    df.to_csv("resume_match_results.csv", index=False)
    print("\nResults saved to 'resume_match_results.csv'.")

# User input for file paths
resume_path = input("Enter the path of the resume (PDF/DOCX): ")
job_description_path = input("Enter the path of the job description (TXT): ")

# Check if files exist
if os.path.exists(resume_path) and os.path.exists(job_description_path):
    process_resume(resume_path, job_description_path)
else:
    print("Error: One or both files do not exist. Please check the file paths.")
