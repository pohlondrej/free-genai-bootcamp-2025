import streamlit as st
import requests
from typing import Optional
import json
from pathlib import Path
import random
import base64

# Backend API URL
BACKEND_URL = "http://localhost:8000"

def create_session():
    """Create new quiz session"""
    response = requests.post(f"{BACKEND_URL}/session/")
    if response.ok:
        return response.json()
    st.error("Failed to create session")
    return None

def play_audio(cache_key: str):
    """Play audio from backend"""
    audio_url = f"{BACKEND_URL}/audio/{cache_key}"
    st.audio(audio_url)

def autoplay_audio(file_url: str):
    """Automatically play audio from URL using HTML audio tag"""
    response = requests.get(file_url)
    audio_bytes = response.content
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

def clear_session_state():
    """Clear all session state variables"""
    st.session_state.intro_played = False
    st.session_state.session = None
    st.session_state.selected_audio = None
    st.session_state.selected_text = None
    st.session_state.matched_pairs = set()
    st.session_state.correct_recalls = set()
    st.session_state.submitted_answer = False
    if "randomized_entries" in st.session_state:
        del st.session_state.randomized_entries

def main():
    st.title("Japanese Learning Assistant")
    
    # Initialize session state variables
    if "intro_played" not in st.session_state:
        st.session_state.intro_played = False
    if "session" not in st.session_state:
        st.session_state.session = None
    if "selected_audio" not in st.session_state:
        st.session_state.selected_audio = None
    if "selected_text" not in st.session_state:
        st.session_state.selected_text = None
    if "matched_pairs" not in st.session_state:
        st.session_state.matched_pairs = set()
    if "correct_recalls" not in st.session_state:
        st.session_state.correct_recalls = set()

    # Show welcome screen if no session
    if not st.session_state.session:
        st.write("""
        Welcome to the Japanese Learning Assistant!
        
        Practice your Japanese listening comprehension through:
        - Vocabulary matching
        - Monologue comprehension
        - Word recall
        """)
        if st.button("Start New Session"):
            with st.spinner("Creating new session..."):
                clear_session_state()  # Clear state before creating new session
                st.session_state.session = create_session()
            st.rerun()
        return

    # Rest of the quiz logic
    if not st.session_state.session:
        st.error("Could not create session")
        return
        
    # Get current stage
    stage = min(st.session_state.session["current_stage"], 3)
    stages = ["Vocabulary", "Comprehension", "Recall"]
    st.progress(min((stage + 1) / len(stages), 1.0))
    if stage < 3:
        st.subheader(f"Stage {stage + 1}: {stages[stage]}")
    
    # Display intro audio on first stage
    if stage == 0:
        if not st.session_state.intro_played:
            audio_url = f"{BACKEND_URL}/audio/{st.session_state.session['en_intro_audio']}"
            autoplay_audio(audio_url)
            st.session_state.intro_played = True
    
    # Display current stage content
    if stage == 0:  # Vocabulary Stage
        vocab_stage = st.session_state.session["vocabulary_stage"]
        
        # Message area for feedback
        message_area = st.empty()
        
        # Show matched pairs count
        total_pairs = len(vocab_stage["entries"])
        matched = len(st.session_state.matched_pairs)
        st.write(f"Matched: {matched}/{total_pairs}")
        
        # Randomize English texts for display
        if "randomized_entries" not in st.session_state:
            entries_copy = vocab_stage["entries"].copy()
            random.shuffle(entries_copy)
            st.session_state.randomized_entries = entries_copy
        
        # Create two columns for audio and text
        audio_col, text_col = st.columns(2)
        
        with audio_col:
            st.subheader("Listen to the words:")
            # Display audio buttons in original order
            for entry in vocab_stage["entries"]:
                button_key = f"audio_{entry['jp_audio']}"
                if entry["jp_audio"] not in st.session_state.matched_pairs:
                    if st.button("🔊", key=button_key):
                        audio_url = f"{BACKEND_URL}/audio/{entry['jp_audio']}"
                        autoplay_audio(audio_url)
                        # Toggle selection
                        if st.session_state.selected_audio == entry["jp_audio"]:
                            st.session_state.selected_audio = None
                        else:
                            st.session_state.selected_audio = entry["jp_audio"]
                else:
                    st.button("✓", key=button_key, disabled=True)
        
        with text_col:
            st.subheader("Match with meanings:")
            # Display text buttons in randomized order
            for entry in st.session_state.randomized_entries:
                text_key = f"text_{entry['en_text']}"
                if entry["jp_audio"] not in st.session_state.matched_pairs:
                    if st.button(entry["en_text"], key=text_key):
                        # Toggle selection
                        if st.session_state.selected_text == entry:
                            st.session_state.selected_text = None
                        else:
                            st.session_state.selected_text = entry
                else:
                    st.button(entry["en_text"], key=text_key, disabled=True)
        
        # Check for matches
        if st.session_state.selected_audio and st.session_state.selected_text:
            if st.session_state.selected_audio == st.session_state.selected_text["jp_audio"]:
                st.session_state.matched_pairs.add(st.session_state.selected_audio)
                message_area.success(f"Correct match! ({matched + 1}/{total_pairs})")
            else:
                message_area.error("Not quite right. Try a different pair!")
            st.session_state.selected_audio = None
            st.session_state.selected_text = None
            st.rerun()
        
        # Show continue button when all pairs are matched
        if len(st.session_state.matched_pairs) >= total_pairs:
            if st.button("Continue to Comprehension"):
                st.session_state.session["current_stage"] = 1  # Set exact stage number
                st.session_state.matched_pairs = set()  # Reset for next session
                st.rerun()

    elif stage == 1:  # Comprehension Stage
        comp_stage = st.session_state.session["comprehension_stage"]
        st.write("Listen to the monologue and answer the question:")
        play_audio(comp_stage["jp_audio"])
        
        answer = st.radio(
            comp_stage["question"],
            ["Yes", "No"],
            key="comprehension_answer"
        )
        
        if "submitted_answer" not in st.session_state:
            st.session_state.submitted_answer = False
        
        if st.button("Submit"):
            is_correct = (answer == "Yes") == comp_stage["correct_answer"]
            if is_correct:
                st.success("✨ Excellent! That's correct!")
                st.session_state.submitted_answer = True
            else:
                st.error("Sorry, that's not correct. Try listening again!")
        
        # Show continue button only after correct answer
        if st.session_state.submitted_answer:
            if st.button("Continue to Recall Stage"):
                st.session_state.session["current_stage"] = 2
                st.session_state.submitted_answer = False  # Reset for next stage
                st.rerun()

    elif stage == 2:  # Recall Stage
        recall_stage = st.session_state.session["recall_stage"]
        st.write("Listen to the continuation and select TWO words that appeared in the audio:")
        play_audio(recall_stage["jp_audio"])
        
        # Create columns for word buttons
        cols = st.columns(3)
        for i, word in enumerate(recall_stage["options"]):
            with cols[i]:
                # Color the button based on selection status
                if word in st.session_state.correct_recalls:
                    st.button(word, key=f"recall_{word}", type="primary", disabled=True)
                elif word == recall_stage["incorrect_option"]:
                    # This is the incorrect word - clear selections if clicked
                    if st.button(word, key=f"recall_{word}", type="secondary"):
                        st.error("Incorrect! This word wasn't in the audio.")
                        st.session_state.correct_recalls.clear()  # Reset on wrong answer
                else:
                    # This is a correct word
                    if st.button(word, key=f"recall_{word}", type="secondary"):
                        st.session_state.correct_recalls.add(word)
                        if len(st.session_state.correct_recalls) == 2:
                            st.success("Well done! You found both correct words!")

        # Show Finish button when two correct words are found
        if len(st.session_state.correct_recalls) == 2:
            if st.button("Finish Session"):
                st.session_state.session["current_stage"] += 1
                st.rerun()

    # Show outro on completion
    if st.session_state.session["current_stage"] >= 3:
        audio_url = f"{BACKEND_URL}/audio/{st.session_state.session['en_outro_audio']}"
        autoplay_audio(audio_url)
        st.write("Congratulations! You've completed the session.")
        if st.button("Back to Main Menu"):
            clear_session_state()  # Clear state before starting new session
            st.rerun()

if __name__ == "__main__":
    main()
