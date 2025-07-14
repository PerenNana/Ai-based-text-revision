Basic AI for Text Revision    

A lightweight and intuitive AI-powered assistant for automatic text revision. From fixing grammar to enhancing style or generating cool versions for your friends — this app does it all through a user-friendly Streamlit interface.


Features
- Grammar Issues – Detects and corrects grammar, spelling, and punctuation errors.

- Style Improvements – Refines sentence structure and expression without altering meaning.

- Mixed Issues – Combines grammar and style correction in one sweep.

- Social Style – Rewrites your text with a fun, friendly tone and emojis — perfect for messages to friends.

- Elegant Style – Elevates your phrasing to sound professional, charming, and smooth.

- Blended Style – Merges casual warmth with elegant flair for perfectly balanced communication.
  

Getting started

1. Install dependencies

  - pip install -r requirements.txt
    

2. Make sure you’ve got the following tools installed:

  - FastAPI

  - Streamlit

  - Ollama – for local LLM processing (e.g. with llama3)
    

3. Launch the backend

  - uvicorn backend:app --reload
    

4. Start Ollama

  - ollama run llama3
    

5. Run the frontend

  - streamlit run app.py
