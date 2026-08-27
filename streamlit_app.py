
import streamlit as st
import requests
from PIL import Image
import os

st.set_page_config(page_title="Fashion Outfit Recommender", layout="centered")
st.title("👗 AI-Powered Fashion Outfit Recommender")

st.markdown("Tell us about yourself and the occasion, and we’ll suggest the perfect outfit!")

# Collect user inputs
gender = st.selectbox("Select Gender", ["Female", "Male", "Unisex"])
age = st.selectbox("Select Age", ["young", "teen", "adult", "old"])
weather = st.selectbox("Select Weather", ["summer", "winter", "all", "Any"])
item_name = st.text_input("Clothing Category (e.g., dress, t-shirt, jeans):")
color = st.text_input("Preferred Color (or type 'Any'):")

if st.button("✨ Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        user_input = {
            "gender": gender.lower(),
            "age": age.lower(),
            "weather": weather.lower(),
            "item_name": item_name.lower().strip(),
            "color": color.lower().strip()
        }

        try:
            response = requests.post("http://127.0.0.1:5000/recommend", json=user_input)
            response.raise_for_status()
            data = response.json()

            if "recommendations" in data and data["recommendations"]:
                st.success("Here are your outfit recommendations:")
                for item in data["recommendations"]:
                    st.image(item["image_name"], caption=item["Description"], use_column_width=True)
            elif "fallback" in data:
                st.warning("No exact matches found. Showing fallback results from Google Images.")
                for item in data["fallback"]:
                    st.image(item["image_name"], caption=item["Description"], use_column_width=True)
            else:
                st.error("No recommendations found.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")            
