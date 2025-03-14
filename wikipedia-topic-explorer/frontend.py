import streamlit as st
import requests
import time
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Wikipedia Topic Explorer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Wikipedia Topic Explorer")
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
                # Article section
                if "article" in result:
                    article = result["article"]
                    st.header(f"📖 {article['title']}")
                    
                    # Create two columns for English and Japanese
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("English")
                        st.write(article["english"])
                        
                    with col2:
                        st.subheader("日本語")
                        st.write(article["japanese"])
                
                # Vocabulary section
                if "vocabulary" in result:
                    st.header("📝 Vocabulary")
                    
                    # Convert vocabulary list to DataFrame for table display
                    vocab_data = []
                    for word in result["vocabulary"]:
                        vocab_data.append({
                            "Word": word["word"],
                            "Reading": word["reading"],
                            "Romaji": word["romaji"],
                            "Meaning": word["meaning"]
                        })
                    
                    if vocab_data:
                        df = pd.DataFrame(vocab_data)
                        # Apply custom styling
                        st.dataframe(
                            df,
                            column_config={
                                "Word": st.column_config.TextColumn(
                                    "Japanese",
                                    help="Japanese word in kanji/kana",
                                    width="medium"
                                ),
                                "Reading": st.column_config.TextColumn(
                                    "Reading",
                                    help="Reading in hiragana",
                                    width="medium"
                                ),
                                "Romaji": st.column_config.TextColumn(
                                    "Romaji",
                                    help="Reading in roman letters",
                                    width="medium"
                                ),
                                "Meaning": st.column_config.TextColumn(
                                    "Meaning",
                                    help="English meaning",
                                    width="large"
                                )
                            },
                            hide_index=True,
                            use_container_width=True
                        )
            else:
                st.error(f"Error: {result['error']}")

st.sidebar.markdown("""
### How it works
1. Enter any topic in English
2. Get a simplified explanation in both English and Japanese
3. Learn relevant vocabulary with readings and meanings

### Features
- 📖 Article summaries in both languages
- 📝 Vocabulary table with readings
- 🔍 Easy-to-read format
""")
