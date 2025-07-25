# streamlit_app.py
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

st.set_page_config(page_title="Nairobi Waste Tracker", layout="centered")

DATA_FILE = 'entries.json'
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

st.title("🗑️ Nairobi Waste Tracker")
st.markdown("Aligned with **SDG 11 (Sustainable Cities)**, **SDG 12 (Responsible Consumption)**, and **SDG 13 (Climate Action)**.")

st.subheader("📋 Submit Waste Collection")

with st.form("waste_form"):
    zone = st.text_input("Zone")
    waste_type = st.selectbox("Waste Type", ["Organic", "Recyclable", "Hazardous", "Landfill"])
    amount = st.number_input("Amount (kg)", min_value=0.1, step=0.1)
    date = st.date_input("Collection Date", value=datetime.today())
    submitted = st.form_submit_button("Submit")

    if submitted:
        new_entry = {
            "zone": zone,
            "waste_type": waste_type,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d")
        }
        with open(DATA_FILE, 'r+') as f:
            data = json.load(f)
            data.insert(0, new_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
        st.success("✅ Entry submitted!")

# Display entries
st.subheader("📊 Recent Entries")

try:
    with open(DATA_FILE) as f:
        entries = json.load(f)
        if entries:
            df = pd.DataFrame(entries)
            st.dataframe(df)
        else:
            st.info("No entries yet.")
except Exception as e:
    st.error(f"Failed to load entries: {e}")
