import streamlit as st
import requests
import os

st.set_page_config(page_title="Auth - FoodForHope", page_icon="🔐", layout="centered")

# Load CSS
with open("frontend/assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://localhost:8000/api"

st.title("🔐 Login / Register")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Welcome Back")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            try:
                response = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["token"] = data["access_token"]
                    st.session_state["role"] = data["role"]
                    st.session_state["user_id"] = data["user_id"]
                    st.success(f"Logged in successfully as {data['role'].capitalize()}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            except Exception as e:
                st.error("Could not connect to the server.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Create an Account")
    role = st.radio("I am a:", ["Donor", "NGO"])
    
    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if role == "Donor":
            full_name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            address = st.text_area("Address")
            col1, col2 = st.columns(2)
            with col1:
                city = st.text_input("City")
                latitude = st.number_input("Latitude", format="%.6f")
            with col2:
                state = st.text_input("State")
                longitude = st.number_input("Longitude", format="%.6f")
            pincode = st.text_input("Pincode")
            
        else: # NGO
            ngo_name = st.text_input("NGO Name")
            reg_num = st.text_input("Registration Number")
            owner_name = st.text_input("Owner Name")
            phone = st.text_input("Phone Number")
            address = st.text_area("Address")
            col1, col2 = st.columns(2)
            with col1:
                city = st.text_input("City")
                latitude = st.number_input("Latitude", format="%.6f")
            with col2:
                state = st.text_input("State")
                longitude = st.number_input("Longitude", format="%.6f")
            pincode = st.text_input("Pincode")
            description = st.text_area("Description")
            working_areas = st.text_input("Working Areas (comma separated)")

        submit_reg = st.form_submit_button("Register")
        
        if submit_reg:
            endpoint = f"{API_URL}/auth/register/{role.lower()}"
            payload = {
                "email": email,
                "password": password,
                "role": role.lower(),
                "phone": phone,
                "address": address,
                "city": city,
                "state": state,
                "pincode": pincode,
                "latitude": latitude,
                "longitude": longitude
            }
            if role == "Donor":
                payload["full_name"] = full_name
            else:
                payload.update({
                    "ngo_name": ngo_name,
                    "registration_number": reg_num,
                    "owner_name": owner_name,
                    "description": description,
                    "working_areas": working_areas
                })
                
            try:
                response = requests.post(endpoint, json=payload)
                if response.status_code == 200:
                    st.success("Registration successful! Please login.")
                else:
                    st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error("Could not connect to the server.")
    st.markdown('</div>', unsafe_allow_html=True)
