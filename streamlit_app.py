import json
import pandas as pd
import traceback
from src.mcq_gen.utils import read_file, extract_mcqs_to_df
import streamlit as st
from src.mcq_gen.MCQ_Gen import generate_quiz

with open(r'C:\Users\afz31\mcq_gen\resp.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.write("Streamlit version:", st.__version__)

#create a title for the app
st.title("Auto MCQ Creator with Langchain and Gemini API") 

#Create a form using st.form
with st.form("user_inputs"):
    #file upload
    uploaded_file=st.file_uploader("upload a PDF or txt file")

    #input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    #subject
    subject=st.text_input("Insert Subject", max_chars=20)

    #Quiz level
    level=st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    #add button
    button = st.form_submit_button("Create MCQs")

    #check if the button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and level:
        with st.spinner("Loading....."):
            try:
                text=read_file(uploaded_file)
                response = generate_quiz(text,mcq_count,subject,level,RESPONSE_JSON)

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("error")
            
            else:
                if isinstance(response, dict):
                    quiz = response.get("updated_quiz")
                    if quiz is not None:
                        table_data = extract_mcqs_to_df(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area(label="Review", value=response.get("complexity_analysis"))
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("Quiz is none")
                else:
                    st.write(response)