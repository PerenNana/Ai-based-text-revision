import streamlit as sl
import requests
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000/revise"

sl.title("✍️ Basic AI For Text Revision")

sl.divider()

# Instructions
with sl.expander("**📘 How to use it?**"):
    sl.markdown("""
    1. Enter your text into the designated area above.
    2. Select the type of revision or formulation you want to receive.
    3. Click the "Get Assistance" button to receive a revised version of your original text.
    """)

sl.markdown("---")

sl.header("Original Text")

with sl.chat_message("user"):
    sl.write("**Original Text**")

user_input = sl.text_area(
    "Enter your text here!", 
    key="original_text",
    height=200,
    help="Enter your text and start the assistance.")

sl.markdown("**📝 Select the type of revision or formulation you want:**")

mode = sl.radio(
    "Select the revision or formulation type you want:",
    options=["Grammar Issues", "Style Improvements", "Mixed Issues", "Social Style", "Elegant Style", "Blended Style"],
    index=1,
    help="Select a type you want."
)

# Button
submit = sl.button("Get Assistance")

sl.markdown("---")

revised_text = ""

if submit:
    if not user_input.strip():
        sl.warning("Please enter some text first.")
    else:
        # Add spinner to simulate thinking
        with sl.spinner("Revising..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "text": user_input,
                        "mode": mode
                    }
                )
                revised = response.json().get("revised_text", "No revision received.")
                sl.session_state.revised_text = revised  # Save to session_state
            except Exception as e:
                sl.session_state.revised_text = f"Error: {e}"

        # Assume `revised_text` is the variable holding the AI response
        if "revised_text" in sl.session_state:
            revised_text = sl.session_state.revised_text
            sl.header("Revised Text")

            with sl.chat_message("assistant"):
                sl.write("**Revised Text**")
            sl.text_area(
                "Here is your revised text:",
                value=revised_text,
                height=200,
                key="revised_text_output",
                help="Copy your revised text with the button beneath.")

        # ⏩ Right-align the copy button using columns
        components.html(f"""
            <script>
            function copyToClipboard() {{
                navigator.clipboard.writeText(document.getElementById("copyTarget").innerText);
                alert("📋 Copied to clipboard!");
            }}
            </script>
            <div style="text-align:right;">
                <button onclick="copyToClipboard()" style="
                    background-color: #262730;
                    color: white;
                    border: 1px solid #5c5c5c;
                    border-radius: 10px;
                    padding: 8px 16px;
                    font-size: 14px;
                    cursor: pointer;
                ">📋 Copy</button>
            </div>
            <div id="copyTarget" style="display:none;">{revised_text}</div>
        """, height=60)

#Task: expand expander after clicking on start revision button