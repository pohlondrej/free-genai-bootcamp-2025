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
        response = requests.post(f"{API_URL}/api/v1/topic", json={"topic": topic})
        job_id = response.json()["job_id"]
        
        # Show progress
        with st.spinner("Processing your request..."):
            # In the dummy version, we'll just wait a second
            time.sleep(1)
            result = requests.get(f"{API_URL}/api/v1/result/{job_id}").json()
            
            # Display results
            st.subheader("English Summary")
            st.write(result["english_summary"])
            
            st.subheader("Japanese Summary")
            st.write(result["japanese_summary"])
            
            st.subheader("Vocabulary")
            for word in result["vocabulary"]:
                st.write(f"• {word['word']} ({word['reading']}) - {word['meaning']}")
            
            st.subheader("Related Images")
            cols = st.columns(2)
            for idx, img_url in enumerate(result["images"]):
                cols[idx % 2].image(img_url, use_column_width=True)

st.sidebar.markdown("""
### How it works
1. Enter any topic in English
2. Get a simplified explanation
3. See the Japanese translation
4. Learn relevant vocabulary
""")
