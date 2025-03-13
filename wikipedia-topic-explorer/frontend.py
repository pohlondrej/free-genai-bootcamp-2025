import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.title("Wikipedia Topic Explorer")
st.write("Enter a topic to get a simplified Japanese explanation and vocabulary list")

# User input
topic = st.text_input("Enter a topic in English:")

if topic:
    if st.button("Generate"):
        # Create job
        response = requests.post(f"{API_URL}/api/v1/topic", json={"english_text": topic})
        job_id = response.json()["job_id"]
        
        # Show progress
        with st.spinner("Processing your request..."):
            while True:
                status = requests.get(f"{API_URL}/api/v1/topic/{job_id}").json()
                if status["status"] == "complete":
                    result = status["result"]
                    break
                elif "error" in status:
                    st.error(f"Error: {status['error']}")
                    break
                time.sleep(1)
            
            # Display results
            if "error" not in result:
                if "translation" in result:
                    st.subheader("Translation")
                    st.write(f"English: {result['translation']['english']}")
                    st.write(f"Japanese: {result['translation']['japanese']}")
                    if "notes" in result["translation"]:
                        st.write(f"Notes: {result['translation']['notes']}")
                
                if "vocabulary" in result:
                    st.subheader("Vocabulary")
                    for word in result["vocabulary"]:
                        st.write(f"• {word['word']} ({word['reading']}) [{word['romaji']}] - {word['meaning']}")
            else:
                st.error(f"Error: {result['error']}")

st.sidebar.markdown("""
### How it works
1. Enter any topic in English
2. Get a Japanese translation
3. Learn relevant vocabulary with readings and meanings
""")
