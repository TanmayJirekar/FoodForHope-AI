import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Donor Dashboard", page_icon="❤️", layout="wide")

# Load CSS
with open("frontend/assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

API_URL = "http://localhost:8000/api"

if "token" not in st.session_state or st.session_state.get("role") != "donor":
    st.warning("Please login as a Donor to view this page.")
    st.stop()

st.title("❤️ Donor Dashboard")

tab1, tab2 = st.tabs(["Donate Food", "My Donations"])

with tab1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Make a New Donation")
    
    with st.form("donation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            food_name = st.text_input("Food Name (e.g., Rice, Bread)")
            food_type = st.selectbox("Food Type", ["Cooked Food", "Packed Food", "Vegetables", "Fruits", "Bakery", "Milk Products", "Dry Food"])
            quantity = st.number_input("Quantity (kg/liters/items)", min_value=0.1)
            persons_served = st.number_input("Approx Persons Served", min_value=1)
            
        with col2:
            preparation_time = st.date_input("Preparation Date")
            prep_time = st.time_input("Preparation Time")
            storage_method = st.selectbox("Storage Method", ["Room Temperature", "Refrigerated", "Frozen"])
            storage_temp = st.number_input("Storage Temperature (°C)")
            packaging_type = st.selectbox("Packaging Type", ["Plastic Container", "Cardboard Box", "Foil", "None"])
            
        st.write("---")
        col3, col4 = st.columns(2)
        with col3:
            expiry_date = st.date_input("Estimated Expiry Date")
            expiry_time = st.time_input("Estimated Expiry Time")
            pickup_address = st.text_area("Pickup Address")
        with col4:
            pickup_date = st.date_input("Pickup Date")
            pickup_time_slot = st.time_input("Pickup Time")
            additional_notes = st.text_area("Additional Notes (Optional)")
            
        image = st.file_uploader("Upload Food Image (Required for AI Safety Check)", type=["jpg", "jpeg", "png", "webp"])
        
        submit_btn = st.form_submit_button("Submit Donation & Run AI Check")
        
        if submit_btn:
            if not image:
                st.error("Please upload an image for AI safety detection.")
            else:
                # Prepare data
                prep_dt = datetime.datetime.combine(preparation_time, prep_time).isoformat()
                exp_dt = datetime.datetime.combine(expiry_date, expiry_time).isoformat()
                pickup_dt = datetime.datetime.combine(pickup_date, pickup_time_slot).isoformat()
                
                payload = {
                    "donor_id": st.session_state["user_id"],
                    "food_name": food_name,
                    "food_type": food_type,
                    "quantity": quantity,
                    "persons_served": persons_served,
                    "preparation_time": prep_dt,
                    "storage_method": storage_method,
                    "storage_temperature": storage_temp,
                    "packaging_type": packaging_type,
                    "expiry_time": exp_dt,
                    "pickup_address": pickup_address,
                    "pickup_time": pickup_dt,
                    "additional_notes": additional_notes
                }
                
                files = {"image": (image.name, image, image.type)}
                headers = {} # Form data doesn't use json Content-Type
                
                with st.spinner("Analyzing food safety with AI..."):
                    try:
                        response = requests.post(f"{API_URL}/donations/create", data=payload, files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"Donation created successfully! AI Safety Score: {data['safety_score']}%")
                            st.info(f"AI Status: {data['safety_status']} | Reason: {data['safety_reason']}")
                            st.info(f"Estimated Safe Time Remaining: {data['safe_time_remaining']} hours")
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Failed to create donation')}")
                    except Exception as e:
                        st.error(f"Failed to connect to the server. {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Donation History")
    
    try:
        response = requests.get(f"{API_URL}/donations/donor/{st.session_state['user_id']}")
        if response.status_code == 200:
            donations = response.json()
            if not donations:
                st.info("No donations found.")
            else:
                for d in donations:
                    with st.expander(f"🍲 {d['food_name']} ({d['status'].capitalize()}) - {d['created_at'][:10]}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Type:** {d['food_type']}")
                            st.write(f"**Quantity:** {d['quantity']} kg")
                            st.write(f"**People Served:** {d['persons_served']}")
                        with col2:
                            st.write(f"**AI Safety Status:** {d['safety_status']}")
                            st.write(f"**Safety Score:** {d['safety_score']}%")
                            st.write(f"**Assigned NGO ID:** {d.get('ngo_id', 'Pending')}")
        else:
            st.error("Failed to load donations.")
    except:
        st.error("Could not connect to server.")
    st.markdown('</div>', unsafe_allow_html=True)
