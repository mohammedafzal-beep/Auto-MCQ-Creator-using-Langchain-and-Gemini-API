import json
import pandas as pd
import traceback
from src.mcq_gen.utils import read_file, extract_mcqs_to_df
import streamlit as st
from src.mcq_gen.MCQ_Gen import generate_quiz

with open(r'C:\Users\afz31\mcq_gen\resp.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.write("Streamlit version:", st.__version__)

#create a title for the app
st.title("Auto MCQ Creator with Langchain and Gemini API")

#Create a form using st.form
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    #input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    #subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #Quiz level
    level = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Easy")

    #add button
    button = st.form_submit_button("Create MCQs")

# Only proceed if the form is submitted and valid data is provided
if button and uploaded_file is not None and mcq_count and subject and level:
    with st.spinner("Loading....."):
        try:
            text = read_file(uploaded_file)
            response = generate_quiz(text, mcq_count, subject, level, RESPONSE_JSON)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error occurred during quiz generation")
        
        else:
            if isinstance(response, dict):
                quiz = response.get("updated_quiz")
                if quiz is not None:
                    table_data = extract_mcqs_to_df(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)
                        st.text_area(label="Review", value=response.get("complexity_analysis"))

                        # Generate downloadable data (CSV, TXT, PDF)
                        csv_data = df.to_csv(index=False)
                        txt_data = df.to_string(index=False)
                        pdf_data = f"Subject: {subject}\nLevel: {level}\n\n" + df.to_string(index=True)

                        # Store data in session state to persist it across reruns
                        st.session_state.csv_data = csv_data
                        st.session_state.txt_data = txt_data
                        st.session_state.pdf_data = pdf_data
                        
                        # Add a flag to indicate that the MCQs are ready
                        st.session_state.mcq_generated = True

# Display download buttons only if MCQs are generated
if 'mcq_generated' in st.session_state and st.session_state.mcq_generated:
    # Create download buttons in parallel using columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download as CSV",
            data=st.session_state.csv_data,
            file_name="mcqs.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            label="Download as TXT",
            data=st.session_state.txt_data,
            file_name="mcqs.txt",
            mime="text/plain"
        )

    with col3:
        st.download_button(
            label="Download as PDF",
            data=st.session_state.pdf_data,
            file_name="mcqs.pdf",
            mime="application/pdf"
        )