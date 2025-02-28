import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
from PIL import Image
import io
import base64

BACKEND_URL = "http://localhost:8000"
CANVAS_WIDTH = 1200  # Full width
CANVAS_HEIGHT = 400  # Less tall

def get_random_word():
    try:
        response = requests.get(f"{BACKEND_URL}/word/random")
        return response.json()["word"]
    except Exception as e:
        st.error("Failed to fetch word from backend")
        return None

def convert_canvas_to_base64(canvas_result):
    if canvas_result is not None and canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

def main():
    st.title("Kana Writing Practice")
    
    # Initialize session state
    if "current_word" not in st.session_state:
        st.session_state.current_word = get_random_word()
        st.session_state.feedback = None
        st.session_state.show_feedback = False
        st.session_state.canvas_key = 0  # Add canvas key to session state

    # Display current word with larger text
    if st.session_state.current_word:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### Draw: {st.session_state.current_word['kana']}")
        with col2:
            st.markdown(f"*Romaji: {st.session_state.current_word['romaji']}*")

    # Canvas spanning full width (no centering columns needed)
    canvas_result = st_canvas(
        fill_color="black",
        stroke_width=14,
        stroke_color="white",
        background_color="black",
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        drawing_mode="freedraw",
        key=f"canvas_{st.session_state.canvas_key}",
    )

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Center the buttons
    _, col1, col2, col3, _ = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        if st.button("Clear"):
            st.session_state.feedback = None
            st.session_state.show_feedback = False
            st.session_state.canvas_key += 1  # Increment key to force canvas reset
            st.rerun()
    
    with col2:
        if st.button("Submit", type="primary"):
            image_data = convert_canvas_to_base64(canvas_result)
            if image_data:
                # For now, just mock the response
                st.session_state.feedback = {"match": True, "detected_text": st.session_state.current_word["kana"]}
                st.session_state.show_feedback = True
                st.rerun()
            else:
                st.error("Please draw something first!")

    with col3:
        if st.button("Next Word"):
            st.session_state.current_word = get_random_word()
            st.session_state.feedback = None
            st.session_state.show_feedback = False
            st.rerun()

    # Show feedback
    if st.session_state.show_feedback and st.session_state.feedback:
        if st.session_state.feedback["match"]:
            st.success("Correct! ✨")
        else:
            st.error(f"Not quite. Try again! Got: {st.session_state.feedback['detected_text']}")

if __name__ == "__main__":
    main()
