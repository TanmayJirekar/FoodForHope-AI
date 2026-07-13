import streamlit as st
import os

st.set_page_config(
    page_title="FoodForHope AI - Smart Food Donation",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("frontend/assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🍲 Welcome to FoodForHope AI")
st.subheader("Smart Food Donation & NGO Management Platform")

st.markdown("""
<div class="hero-container">
    <h3>Reduce food wastage and hunger with AI</h3>
    <p>Connect with local NGOs, donate surplus food safely, and track your impact in real-time. Our AI Food Safety Detection ensures only safe and fresh food reaches those in need.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📸 AI Food Safety</h4>
        <p>Advanced CNN models scan your food images to detect spoilage and estimate freshness.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📍 Smart NGO Matching</h4>
        <p>Our Recommendation Engine connects you with the nearest NGOs based on real-time demand.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Impact Tracking</h4>
        <p>Monitor how many people you've fed and view real-time analytics of your donations.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.write("### Get Started")
st.info("👈 Please select a page from the sidebar to login, register, or access your dashboard.")
