import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ---------------- LOAD FILES ----------------
df = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")

st.title("💻 Laptop Price Predictor")
st.write("Enter laptop specifications to predict the price")

# ---------------- USER INPUTS ----------------

company = st.selectbox("Brand", df['company'].unique())
typename = st.selectbox("Laptop Type", df['typename'].unique())
os_system = st.selectbox("Operating System", df['os_system'].unique())
cpu_name = st.selectbox("CPU", df['Cpu_Name'].unique())
gpu_brand = st.selectbox("GPU Brand", df['gpu_brand'].unique())

ram = st.selectbox("RAM (in GB)", [2,4,6,8,12,16,24,32,64])
weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1)

touchscreen = st.selectbox("Touchscreen", ["No", "Yes"])
ips = st.selectbox("IPS Display", ["No", "Yes"])
full_hd = st.selectbox("Full HD", ["No", "Yes"])
# resolution = st.selectbox('Screen Resolution',['1920x1080', '1366x768', '1600x900', '3840x2160','3200x1800', '2880x1800', '2560x1600',
#         '2560x1440', '2304x1440'])
ppi = st.number_input("PPI", min_value=80.0, max_value=400.0)

hdd = st.number_input("HDD (GB)", min_value=0, max_value=2000, step=128)
ssd = st.number_input("SSD (GB)", min_value=0, max_value=2000, step=128)

# ---------------- PREPROCESS INPUT ----------------

if st.button("Predict Price 💰"):
    input_df = pd.DataFrame([[
        company,
        typename,
        ram,
        os_system,
        weight,
        1 if touchscreen == "Yes" else 0,
        1 if ips == "Yes" else 0,
        1 if full_hd == "Yes" else 0,
        ppi ,
        cpu_name,
        hdd,
        ssd,
        gpu_brand
    ]], columns=[
        'company',
        'typename',
        'ram',
        'os_system',
        'weight',
        'Touchscreen',
        'IPS Panel',
        'full_HD',
        'ppi',
        'Cpu_Name',
        'HDD',
        'SSD',
        'gpu_brand'
    ])

    # Predict (log price)
    log_price = pipe.predict(input_df)

    # Convert back to actual price
    price = int(np.exp(log_price)[0])

    st.success(f"💸 Estimated Laptop Price: ₹ {price:,}")
