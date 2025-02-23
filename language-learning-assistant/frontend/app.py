import streamlit as st
import requests
from typing import Optional
import json
from pathlib import Path
import random

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

def main():
    st.title("Japanese Learning Assistant")
    
    # Initialize session state variables
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
        play_audio(st.session_state.session["en_intro_audio"])
    
    # Display current stage content
    if stage == 0:  # Vocabulary Stage
        vocab_stage = st.session_state.session["vocabulary_stage"]
        
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
                        play_audio(entry["jp_audio"])
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
                        st.session_state.selected_text = entry
                else:
                    st.button(entry["en_text"], key=text_key, disabled=True)
        
        # Check for matches
        if st.session_state.selected_audio and st.session_state.selected_text:
            if st.session_state.selected_audio == st.session_state.selected_text["jp_audio"]:
                st.session_state.matched_pairs.add(st.session_state.selected_audio)
                st.success("Correct match!")
            else:
                st.error("Try again!")
            # Reset selections
            st.session_state.selected_audio = None
            st.session_state.selected_text = None
            st.rerun()
        
        # Show continue button when all pairs are matched
        if len(st.session_state.matched_pairs) == len(vocab_stage["entries"]):
            if st.button("Continue to Comprehension"):
                st.session_state.session["current_stage"] += 1
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
        
        if st.button("Submit"):
            is_correct = (answer == "Yes") == comp_stage["correct_answer"]
            if is_correct:
                st.success("Correct!")
            else:
                st.error("Incorrect.")
            st.session_state.session["current_stage"] += 1
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
                    if st.button(word, key=f"recall_{word}", type="secondary"):
                        st.error("Incorrect! This word wasn't in the audio.")
                else:
                    if st.button(word, key=f"recall_{word}", type="secondary"):
                        st.session_state.correct_recalls.add(word)
                        if len(st.session_state.correct_recalls) == 2:
                            st.success("Well done! You found both words!")

        # Show Finish button when two correct words are found
        if len(st.session_state.correct_recalls) == 2:
            if st.button("Finish Session"):
                st.session_state.session["current_stage"] += 1
                st.rerun()

    # Show outro on completion
    if st.session_state.session["current_stage"] >= 3:
        play_audio(st.session_state.session["en_outro_audio"])
        if st.button("Start New Session"):
            del st.session_state.session
            st.rerun()

if __name__ == "__main__":
    main()
