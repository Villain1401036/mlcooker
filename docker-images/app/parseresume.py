import re
import spacy
from spacy.matcher import Matcher
from pypdf import PdfReader
from skills import skills_list
import requests
import os

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    text = ""
    for i in range(number_of_pages):
        page = reader.pages[i]
        text_p = page.extract_text()
        if text_p:
            text += text_p
    return text

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number

def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email

def extract_skills_from_resume(text, skills_list):
    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills

def extract_education_from_resume(text):
    education = []

    # Use regex pattern to find education information
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())

    return education

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    # Define name patterns
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
        # Add more patterns as needed
    ]

    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text

    return None

def parse_resume(pdf_url=None):
        
        output_directory = "./rawdata"
        resume_path = download_pdf_from_link(pdf_url, output_directory)
        if resume_path:
            print("Resume downloaded successfully:", resume_path)
        else:
            print("Failed to download the resume.")
        # resume_path = "./rawdata/resume.pdf"
        resume_path = "./rawdata/resume.pdf"

        res_dir = {}
        text = extract_text_from_pdf(resume_path)
        # print("asdasdasd",extract_text_from_pdf(resume_path))
        print("Resume:", resume_path)
        
        name = extract_name(text)
        res_dir['name'] = name


        contact_number = extract_contact_number_from_resume(text)
        res_dir['contact_number'] = contact_number

        email = extract_email_from_resume(text)
        res_dir['email'] = email

        extracted_skills = extract_skills_from_resume(text, skills_list)
        res_dir['skills'] = extracted_skills

        extracted_education = extract_education_from_resume(text)
        res_dir['education'] = extracted_education
        
        return res_dir

def download_pdf_from_link(url, output_dir):
            response = requests.get(url)
            if response.status_code == 200:
                filename = os.path.join(output_dir, "resume.pdf")
                with open(filename, "wb") as file:
                    file.write(response.content)
                return filename
            else:
                return None

        # Example usage:
        

if __name__ == "__main__":
    
    
    print(parse_resume())