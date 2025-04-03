#

import streamlit as st
import requests

st.title("AI Health Chatbot")

name = st.text_input("Enter your name:")
symptoms = st.text_area("Describe your symptoms:")

if st.button("Analyze Symptoms"):
    if name and symptoms:
        response = requests.post("http://127.0.0.1:5000/submit_patient_data", 
                                 json={"name": name, "symptoms": symptoms})
        result = response.json()
        st.write(f"Risk Level: {result['risk']}")
        st.success(result['message'])
    else:
        st.warning("Please enter all details.")
