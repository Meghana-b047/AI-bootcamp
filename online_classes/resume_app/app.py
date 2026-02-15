#phase 1: Extract data from the resume pdf in markdown language.
from PyPDF2 import PdfReader 
#from docx import Document

def extract_text(): 

    resume_filename = input("Please enter the name of the resume pdf: ")

    doc = PdfReader(resume_filename)

    text_file = f"{resume_filename.split(".")[0]}.txt"

    with open(text_file, 'w') as file2: 

        for page in doc.pages: 
            line = page.extract_text()
            file2.write(line)

    return text_file

if __name__=='__main__': 

    extract_text()