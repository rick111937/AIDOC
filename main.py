import streamlit as st
from symptom_analyzer import analyze_symptoms
from location_finder import find_nearest_center
from tts_engine import speak_response

st.set_page_config(page_title="AI Rural Health Assistant", page_icon="🏥")
st.title("MEDISURE 🏥")

# User input (text)
user_input = st.text_input("Describe your symptoms in your language:")

if st.button("Analyze"):
    if user_input.strip():
        illness = analyze_symptoms(user_input)
        health_center = find_nearest_center("YourVillageName")

        st.subheader("Possible Illness:")
        st.write(illness)

        st.subheader("Nearest Health Center:")
        st.write(health_center)

        speak_response(f"Aapko {illness} ho sakta hai. Kripya {health_center} jayein.")
    else:
        st.warning("Please enter your symptoms.")

# 2️⃣ symptom_analyzer.py - NLP Modelfg
from transformers import pipeline

classifier = pipeline("text-classification", model="joeddav/xlm-roberta-large-xnli")

# Very simple example mapping
SYMPTOM_MAP = {
    "fever": "Malaria or Dengue",
    "cough": "Common Cold or TB",
    "headache": "Migraine or Viral Fever"
}

def analyze_symptoms(text):
    result = classifier(text)
    for keyword, illness in SYMPTOM_MAP.items():
        if keyword in text.lower():
            return illness
    return "General Check-up Suggested"

# 3️⃣ location_finder.py - Nearest Center Lookup
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

HEALTH_CENTERS = [
    {"name": "XYZ Govt Clinic", "lat": 22.57, "lon": 88.36},
    {"name": "ABC Primary Health Center", "lat": 22.60, "lon": 88.38}
]

def find_nearest_center(village):
    geolocator = Nominatim(user_agent="health-bot")
    location = geolocator.geocode(village)
    if not location:
        return "No health center found."

    user_coords = (location.latitude, location.longitude)
    nearest = min(HEALTH_CENTERS, key=lambda c: geodesic(user_coords, (c['lat'], c['lon'])).km)
    return f"{nearest['name']} ({round(geodesic(user_coords, (nearest['lat'], nearest['lon'])).km, 1)} km)"

# 4️⃣ tts_engine.py - Text-to-Speech
from gtts import gTTS
import os

def speak_response(text):
    tts = gTTS(text, lang="hi")
    file_path = "response.mp3"
    tts.save(file_path)
    os.system(f"start {file_path}") 
