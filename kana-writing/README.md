# Kana Writing Practice App

## Overview
A simple web-based application for practicing Japanese kana writing. Users are presented with random Japanese words (in kana only), which they must draw on a canvas. The app uses OCR to verify if the drawing matches the prompt.

For detailed technical specifications, API documentation, and implementation details, see:
- [Project Technical Documentation](docs/Project.md)
- [Implementation Tasks](docs/Tasks.md)
- [Future Improvements](docs/Improvements.md)

## Screenshots
<img src="docs/images/image.png" alt="Kana Writing Practice App" height="400"/>

## Key Features
- Random kana word generation
- Drawing canvas for user input
- OCR-based verification
- Immediate feedback (match/no match)

## Quick Start
1. Create a conda environment:
   ```bash
   conda create -n kana-practice python=3.10
   conda activate kana-practice
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the services:
   ```bash
   python start.py
   ```

4. Access:
   - Backend API: http://localhost:8000/docs
   - Frontend: http://localhost:8501