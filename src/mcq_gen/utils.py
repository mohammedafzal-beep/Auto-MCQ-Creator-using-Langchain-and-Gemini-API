import PyPDF2
import traceback
import re

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def extract_mcqs_to_df(quiz_str):
    try:
        # Regular expression to extract MCQs, options, and answers
        pattern = r'"mcq": "(.*?)".*?"options": \{(.*?)\}.*?"correct": "(.*?)"'

        # Find all matches
        matches = re.findall(pattern, quiz_str, re.DOTALL)

        # Process each match
        quiz_data = []
        for mcq, options_str, correct in matches:
            # Extract individual options
            options_pattern = r'"([a-d])": "(.*?)"'
            options = re.findall(options_pattern, options_str)

            # Create a dictionary for the question
            question = {
                "mcq": mcq.strip(),
                "options": {key: value.strip() for key, value in options},
                "correct": correct.strip(),
            }
            quiz_data.append(question)
        
        return quiz_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False