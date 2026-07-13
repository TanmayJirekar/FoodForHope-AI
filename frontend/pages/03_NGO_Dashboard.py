import streamlit as st
import requests

st.set_page_config(page_title="NGO Dashboard", page_icon="🏢", layout="wide")

# Load CSS
with open("frontend/assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://localhost:8000/api"

if "token" not in st.session_state or st.session_state.get("role") != "ngo":
    st.warning("Please login as an NGO to view this page.")
    st.stop()

st.title("🏢 NGO Dashboard")

tab1, tab2 = st.tabs(["Available Donations", "My Pickups"])

with tab1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Food Donations Available Nearby")
    st.info("In a full production environment, this would list unassigned donations filtered by your location.")
    # For demo purposes, we would fetch unassigned donations here.
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Manage Pickups")
    st.write("View and update status for your accepted donations.")
    st.markdown('</div>', unsafe_allow_html=True)
