import streamlit as st
import requests
from PIL import Image
import io
import base64

BACKEND_URL = "http://localhost:8000"

def get_random_word():
    try:
        response = requests.get(f"{BACKEND_URL}/word/random")
        return response.json()["word"]
    except Exception as e:
        st.error("Failed to fetch word from backend")
        return None

def main():
    st.title("Kana Writing Practice")
    
    if "current_word" not in st.session_state:
        st.session_state.current_word = get_random_word()

    # Display current word
    if st.session_state.current_word:
        st.header(f"Draw: {st.session_state.current_word['kana']}")
        st.caption(f"Romaji: {st.session_state.current_word['romaji']}")
    
    # TODO: Add canvas
    # TODO: Add submit button
    # TODO: Add clear button
    
    if st.button("Next Word"):
        st.session_state.current_word = get_random_word()
        st.rerun()

if __name__ == "__main__":
    main()
