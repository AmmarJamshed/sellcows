#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from web3 import Web3
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="🐄 Cow Marketplace – AI & Blockchain", layout="wide")

# ------------------ Styling ------------------ #
st.markdown("""
    <style>
    body {
        background-color: #f4f4f9;
    }
    .stApp {
        background-color: #f4f4f9;
        color: #333333;
    }
    h1, h2, h3, h4 {
        color: #4B0082;
    }
    .stButton>button {
        background-color: #00FFAA;
        color: black;
        font-weight: bold;
        border-radius: 10px;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐄 CowFarm Consumer Portal – Buy, Sell, and Forecast")

# ------------------ Wallet Input ------------------ #
st.subheader("🔗 Enter Your MetaMask Wallet Address")
w_address = st.text_input("Wallet Address", placeholder="0x...")
if w_address:
    st.success(f"✅ Wallet Connected: {w_address}")
else:
    st.warning("🦊 Please enter your MetaMask wallet address manually.")

# ------------------ Ethereum Connection ------------------ #
infura_url = "https://sepolia.infura.io/v3/40915988fef54b268deda92af3e2ba66"
web3 = Web3(Web3.HTTPProvider(infura_url))
if web3.is_connected():
    st.success("✅ Connected to Sepolia Testnet via Infura")
else:
    st.error("❌ Failed to connect to Ethereum")

# ------------------ Load ABI ------------------ #
try:
    with open("CowFarm.json") as f:
        contract_json = json.load(f)
        abi = contract_json["abi"]
except Exception as e:
    st.error(f"Error loading ABI: {e}")
    st.stop()

contract_address = "0x0C5996E38D7B3b00e15F916AafF7Ef987a1A90f1"
try:
    contract = web3.eth.contract(address=contract_address, abi=abi)
except Exception as e:
    st.error(f"Error creating contract instance: {e}")
    st.stop()

# ------------------ Buy/Sell Marketplace ------------------ #
st.header("🛒 Buy & Sell Cows")
st.markdown("Check cow details below, validated with Animal Passport and IoT Tag health metrics.")

sample_data = pd.DataFrame({
    "Cow ID": [101, 102, 103],
    "Breed": ["Sahiwal", "Jersey", "Friesian"],
    "Age (mo)": [36, 24, 48],
    "Weight (kg)": [350, 400, 450],
    "Health Score": [9.0, 8.5, 7.8],
    "IoT Verified": ["✅", "✅", "✅"],
    "Animal Passport": ["Available", "Available", "Available"],
    "Current Price (PKR)": [75000, 82000, 88000],
})
st.dataframe(sample_data, use_container_width=True)

selected_id = st.selectbox("Select Cow ID to Buy", sample_data["Cow ID"])
if st.button("🐄 Buy This Cow"):
    st.success(f"✅ Cow #{selected_id} has been added to your wallet (simulation).")

# ------------------ Choose Farm to Store ------------------ #
st.header("🏠 Choose a Farm to Store Your Cow")
farm_data = pd.DataFrame({
    "Farm Name": ["GreenPasture", "DairyHub", "OrganicHeards"],
    "Location": ["Lahore", "Faisalabad", "Sahiwal"],
    "Monthly Fee (PKR)": [1500, 1200, 1800],
    "Vacant Slots": [10, 6, 3],
})
st.dataframe(farm_data, use_container_width=True)
selected_farm = st.selectbox("Choose a Farm", farm_data["Farm Name"])
if st.button("📦 Store Cow at Selected Farm"):
    st.success(f"🐄 Cow stored at {selected_farm}. Monthly fee applied.")

# ------------------ Monthly AI Forecast ------------------ #
st.header("📊 Monthly Cow Price Forecast")

selected_cow = st.selectbox("Select Your Cow ID", sample_data["Cow ID"])

if st.button("📈 Show Forecasted Prices"):
    try:
        cow_row = sample_data[sample_data["Cow ID"] == selected_cow].iloc[0]
        features = pd.DataFrame([[0, cow_row["Age (mo)"], cow_row["Weight (kg)"], cow_row["Health Score"], 12]],
                                columns=["breed", "age", "weight", "health", "milk"])
        model = RandomForestRegressor()
        model.fit(np.array([[0, 24, 300, 8.0, 10]]), [70000])  # dummy model
        forecasted_price = model.predict(features)[0] + 1000  # simulate monthly change
        gov_adjustment = -500
        final_price = forecasted_price + gov_adjustment
        st.success(f"📅 Forecasted Monthly Price: PKR {int(final_price):,} (Gov Control Adjusted)")
    except Exception as e:
        st.error(f"Forecasting error: {e}")

