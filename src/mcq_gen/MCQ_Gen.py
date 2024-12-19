import os
import json
import pandas as pd
from PyPDF2 import PdfReader

file_path = r"C:\Users\afz31\mcq_gen\data.txt"
with open(file_path, 'r') as file:
    text = file.read()

response_json = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

prompt=f"""
{text}
Create some unique MCQs in json string like below:
{response_json}
"""

from huggingface_hub import InferenceClient

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

KEY=os.getenv("KEY")

# Initialize the client
client = InferenceClient(api_key=KEY)

# Define the message
messages = [
    {
        "role": "user",
        "content": prompt
    }
]

# Attempt to get a response
completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-72B-Instruct",
    messages=messages,
)

quiz = completion.choices[0].message.content

import re

# Regex to extract questions, options, and answers
pattern = r'"(\d+)": {\s*"mcq": "(.*?)",\s*"options": {\s*"a": "(.*?)",\s*"b": "(.*?)",\s*"c": "(.*?)",\s*"d": "(.*?)"\s*},\s*"correct": "(.*?)"\s*}'

matches = re.findall(pattern, quiz)

# Create a list of dictionaries to store the MCQs
mcqs = []
for match in matches:
    question, option_a, option_b, option_c, option_d, answer_key, answer_text = match
    mcqs.append({
        "question": question.strip(),
        "options": {
            "A": option_a.strip(),
            "B": option_b.strip(),
            "C": option_c.strip(),
            "D": option_d.strip()
        },
        "answer": {
            "key": answer_key.strip(),
            "text": answer_text.strip()
        }
    })

# Convert the MCQs list to a JSON string
mcqs_json = json.dumps(mcqs, indent=4)

data = []
for mcq in mcqs:
    data.append({
        "question": mcq["question"],
        "option_A": mcq["options"]["A"],
        "option_B": mcq["options"]["B"],
        "option_C": mcq["options"]["C"],
        "option_D": mcq["options"]["D"],
        "answer_key": mcq["answer"]["key"],
        "answer_text": mcq["answer"]["text"]
    })

# Create the DataFrame
df = pd.DataFrame(data)

df.to_csv("quiz_data.csv",index=False)