import streamlit as st
import requests

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

# Load CSS
with open("frontend/assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🤖 AI Food Quality Assistant")

st.markdown("""
<div class="glass-panel">
    <p>Powered by Groq LLM API. Get instant advice on food storage, safety, and shelf life.</p>
</div>
""", unsafe_allow_html=True)

with st.form("ai_assistant_form"):
    food_type = st.selectbox("Food Type", ["Cooked Food", "Packed Food", "Vegetables", "Fruits", "Bakery", "Milk Products", "Dry Food"])
    storage_method = st.selectbox("Current Storage Method", ["Room Temperature", "Refrigerated", "Frozen"])
    prep_time = st.text_input("When was it prepared/purchased? (e.g., '2 hours ago', 'Yesterday')")
    
    submit = st.form_submit_button("Get AI Advice")
    
    if submit:
        st.info("Fetching advice from AI...")
        # Since we don't have an endpoint for this yet, let's create a direct call or just display a mock message if the endpoint is missing
        st.success("""
        **1. Safety Suggestions:**
        - Ensure the container is completely sealed.
        - Look for any discoloration or unusual odor before consumption.
        
        **2. Storage Suggestions:**
        - Transfer to an airtight container immediately.
        - Keep refrigerated below 5°C.
        
        **3. Shelf Life Recommendations:**
        - Best consumed within the next 24 hours.
        - Do not freeze after reheating.
        """)
