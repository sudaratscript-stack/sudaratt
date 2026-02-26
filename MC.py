# -*- coding: utf-8 -*-
"""
Classification App
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Classification App", layout="wide")

# ---------------- LOAD MODELS ---------------- #
used_car_model = pickle.load(open('Used_cars_model.sav','rb'))
riding_model = pickle.load(open('RidingMowers_model.sav','rb'))

# ---------------- MAP DATA ---------------- #
fuel_map = {
    'Diesel': 0,
    'Electric': 1,
    'Petrol': 2
}

engine_map = {
    '800': 0, '1000': 1, '1200': 2, '1500': 3,
    '1800': 4, '2000': 5, '2500': 6,
    '3000': 7, '4000': 8, '5000': 9
}

brand_map = {
    'BMW': 0, 'Chevrolet': 1, 'Ford': 2,
    'Honda': 3, 'Hyundai': 4, 'Kia': 5,
    'Nissan': 6, 'Tesla': 7,
    'Toyota': 8, 'Volkswagen': 9
}

transmission_map = {
    'Automatic': 0,
    'Manual': 1
}

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    selected = option_menu(
        "Prediction",
        ["Ridingmower", "Used_cars", "BMI"],
        icons=["activity", "car-front", "heart-pulse"],
        menu_icon="cast",
        default_index=0
    )

# ================= RIDING ================= #
if selected == "Ridingmower":

    st.title("Riding Mower Classification")

    Income = st.text_input("Income")
    LotSize = st.text_input("Lot Size")

    if st.button("Predict"):

        prediction = riding_model.predict([[float(Income), float(LotSize)]])

        if prediction[0] == 1:
            result = "Owner"
        else:
            result = "Non Owner"

        st.success(result)

# ================= USED CARS ================= #
if selected == "Used_cars":

    st.title("ประเมินราคารถมือ 2")

    make_year = st.text_input("ปีที่ผลิต")
    mileage_kmpl = st.text_input("KM/L")
    engine_cc = st.selectbox("ขนาดเครื่องยนต์ (CC)", list(engine_map.keys()))
    fuel_type = st.selectbox("ประเภทน้ำมัน", list(fuel_map.keys()))
    owner_count = st.text_input("จำนวนเจ้าของเดิม")
    brand = st.selectbox("ยี่ห้อรถ", list(brand_map.keys()))
    transmission = st.selectbox("ประเภทเกียร์", list(transmission_map.keys()))
    accidents_reported = st.text_input("จำนวนอุบัติเหตุ")

    if st.button("Predict"):

        prediction = used_car_model.predict([[
            float(make_year),
            float(mileage_kmpl),
            engine_map[engine_cc],
            fuel_map[fuel_type],
            float(owner_count),
            brand_map[brand],
            transmission_map[transmission],
            float(accidents_reported)
        ]])

        price = round(prediction[0], 2)

        st.success(f"ราคาประเมิน: {price} บาท")

# ================= BMI ================= #
if selected == "BMI":

    st.title("BMI Classification")

    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

    if st.button("Predict"):

        height_m = height / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            result = "Underweight (ผอม)"
        elif 18.5 <= bmi < 25:
            result = "Normal (ปกติ)"
        elif 25 <= bmi < 30:
            result = "Overweight (ท้วม)"
        else:
            result = "Obese (อ้วน)"

        st.success(f"BMI = {round(bmi,2)} → {result}")
