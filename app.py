import streamlit as st
import speech_recognition as sr
import urllib.parse
from gtts import gTTS
from symptom_analyzer import analyze_symptoms
import os
import time
import requests
import xml.etree.ElementTree as ET
from langdetect import detect
import pyperclip
import streamlit.components.v1 as components                    # python -m streamlit run app.py
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
from fpdf import FPDF
import random
from twilio.rest import Client
import datetime
import pandas as pd
API_KEY = "1e870627819e31d45467aeb1cb33bdae"  
st.set_page_config(
    page_title="🧠 AIDOC – Your Smart AI Health Assistant",
    page_icon="⚕️",
    layout="wide"
)

# Custom CSS

st.markdown("""
<style>
/* ============================================
   PREMIUM ANIMATED BACKGROUND
   ============================================ */

@keyframes gradientShift {
    0% {
        background-position: 0% 50%;
        filter: hue-rotate(0deg);
    }
    25% {
        background-position: 100% 50%;
    }
    50% {
        background-position: 100% 100%;
    }
    75% {
        background-position: 0% 0%;
    }
    100% {
        background-position: 0% 50%;
        filter: hue-rotate(0deg);
    }
}

@keyframes float-particle {
    0% {
        transform: translateY(100vh) translateX(0) scale(1);
        opacity: 0;
    }
    10% {
        opacity: 0.7;
    }
    90% {
        opacity: 0.7;
    }
    100% {
        transform: translateY(-100vh) translateX(100px) scale(0.5);
        opacity: 0;
    }
}

@keyframes pulse-bg {
    0%, 100% {
        box-shadow: inset 0 0 60px rgba(0, 212, 255, 0.05);
    }
    50% {
        box-shadow: inset 0 0 80px rgba(0, 212, 255, 0.1);
    }
}

/* Main Background Container */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(ellipse at 20% 50%, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0, 153, 255, 0.1) 0%, transparent 50%),
        radial-gradient(ellipse at 40% 0%, rgba(100, 150, 255, 0.08) 0%, transparent 60%),
        linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #0f0f1e 100%);
    background-size: 400% 400%, 600% 600%, 500% 500%, 100% 100%;
    animation: gradientShift 15s ease infinite;
    z-index: 0;
    pointer-events: none;
}

/* Animated Background Blur Layer */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        url('data:image/svg+xml,<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" result="noise" seed="2"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/></filter><rect width="100" height="100" fill="rgba(0,212,255,0.02)" filter="url(%23noise)"/></svg>'),
        linear-gradient(0deg, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.1));
    background-size: 200% 200%, 100% 100%;
    animation: pulse-bg 4s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
    backdrop-filter: blur(1px);
}

/* Ensure content is above background */
[data-testid="stAppViewContainer"] {
    background: transparent;
    position: relative;
    z-index: 1;
}

/* Dark gradient overlay */
[data-testid="stAppViewContainer"] {
    color: #ecf0f1;
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Remove Streamlit default header */
[data-testid="stHeader"] {
    background: transparent;
    box-shadow: none;
    z-index: 10;
}

/* Section styling */
.section {
    padding: 100px 20px;
    margin-top: 60px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.6);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.08);
    animation: fadeIn 1.2s ease-in-out;
    position: relative;
    z-index: 2;
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Floating Particles Effect */
.particle {
    position: fixed;
    width: 4px;
    height: 4px;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.8), rgba(0, 153, 255, 0.2));
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    animation: float-particle 20s ease-in infinite;
    backdrop-filter: blur(2px);
}

@keyframes fadeIn {
    from { 
        opacity: 0;
        transform: translateY(30px);
    }
    to { 
        opacity: 1;
        transform: translateY(0);
    }
}

/* Subtle mesh gradient effect */
body {
    background: transparent;
    overflow-x: hidden;
}
</style>

<!-- Floating Particles -->
<div class="particle" style="left: 10%; animation-delay: 0s; animation-duration: 25s;"></div>
<div class="particle" style="left: 20%; animation-delay: 2s; animation-duration: 30s;"></div>
<div class="particle" style="left: 30%; animation-delay: 4s; animation-duration: 22s;"></div>
<div class="particle" style="left: 40%; animation-delay: 6s; animation-duration: 28s;"></div>
<div class="particle" style="left: 50%; animation-delay: 8s; animation-duration: 24s;"></div>
<div class="particle" style="left: 60%; animation-delay: 10s; animation-duration: 26s;"></div>
<div class="particle" style="left: 70%; animation-delay: 12s; animation-duration: 23s;"></div>
<div class="particle" style="left: 80%; animation-delay: 14s; animation-duration: 27s;"></div>
<div class="particle" style="left: 90%; animation-delay: 16s; animation-duration: 25s;"></div>
""", unsafe_allow_html=True)

st.markdown("""<style>
.health-title {
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 35px;
    letter-spacing: 1px;
    background: linear-gradient(90deg, #4facfe, #00f2fe, #38ef7d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0px 0px 20px rgba(79,172,254,0.6);
    animation: glowPulse 2s infinite alternate;
}

@keyframes glowPulse {
    from { text-shadow: 0 0 8px #4facfe, 0 0 18px #00f2fe; }
    to { text-shadow: 0 0 20px #4facfe, 0 0 35px #38ef7d; }
}

/* =========================
   PROGRESS RINGS (Smartwatch Style)
   ========================= */
.progress-ring {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: conic-gradient(var(--color) calc(var(--percent)*1%), #1c1f2b 0);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px auto;
    box-shadow: 0 0 20px rgba(0,0,0,0.6), 0 0 30px rgba(0,242,254,0.2);
    position: relative;
    transition: all 0.4s ease;
}

.progress-ring:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(0,242,254,0.5), 0 0 50px rgba(79,172,254,0.4);
}

.progress-ring::before {
    content: "";
    position: absolute;
    width: 115px;
    height: 115px;
    background: #0a0f1c;
    border-radius: 50%;
    z-index: 1;
    box-shadow: inset 0 0 15px rgba(0,242,254,0.2);
}

.progress-value {
    position: relative;
    z-index: 2;
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
    text-shadow: 0 0 10px rgba(0,242,254,0.7);
}

/* =========================
   INPUT FIELDS
   ========================= */
input[type=number] {
    border: 2px solid #4facfe !important;
    border-radius: 12px !important;
    padding: 12px !important;
    background: rgba(10,15,28,0.85) !important;
    color: white !important;
    font-size: 1rem !important;
    transition: all 0.3s ease-in-out;
}

input[type=number]:focus {
    outline: none !important;
    border-color: #00f2fe !important;
    box-shadow: 0 0 15px #00f2fe, 0 0 25px rgba(79,172,254,0.5);
}

/* =========================
   ALERTS
   ========================= */
div.stAlert {
    border-radius: 16px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 18px !important;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    animation: slideUp 0.6s ease;
}

@keyframes slideUp {
    from {opacity: 0; transform: translateY(25px);}
    to {opacity: 1; transform: translateY(0);}
}

}                        
</style>
""", unsafe_allow_html=True)



# --- Sidebar Branding ---
st.sidebar.markdown("""
<style>
.sidebar-glass {
    background: linear-gradient(120deg,rgba(37,99,235,0.13) 0%,rgba(6,182,212,0.13) 100%);
    border-radius: 28px;
    box-shadow: 0 6px 32px rgba(60,130,246,0.13);
    padding: 24px 18px 18px 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
    position: relative;
}
.sidebar-glass .sidebar-icon {
    position: absolute;
    top: 18px;
    right: 18px;
    width: 38px;
    height: 38px;
    opacity: 0.8;
    animation: floatIcon 3.5s infinite ease-in-out;
}
@keyframes floatIcon {
    0% { transform: translateY(0); }
    50% { transform: translateY(-12px) scale(1.08); }
    100% { transform: translateY(0); }
}
</style>
<div class='sidebar-glass' style='display:flex;flex-direction:column;align-items:center;gap:10px;'>
    <img src='https://img.icons8.com/ios-filled/96/4a90e2/doctor-male.png' alt='AI Health Logo' style='width:72px;animation:logo-bounce 2s infinite;margin-bottom:6px;box-shadow:0 2px 10px rgba(60,130,246,0.10);'>
    <h2 style='margin:0;font-size:1.35rem;color:#2563eb;font-weight:800;letter-spacing:1px;'>AI Health Assistant</h2>
    <span style='font-size:1rem;color:#06b6d4;font-weight:500;display:block;margin-bottom:6px;'>Your Smart Medical Companion</span>
    <span style='background:rgba(255,255,255,0.6);padding:5px 12px;border-radius:12px;box-shadow:0 1px 4px rgba(60,130,246,0.07);font-size:0.95rem;color:#2563eb;display:flex;align-items:center;gap:4px;'>
        <img src='https://img.icons8.com/color/20/artificial-intelligence.png' style='vertical-align:middle;'> Powered by AI
    </span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    👋 **Welcome!**  
    This app helps you detect possible illnesses based on your symptoms and location.  
    🧠 Powered by AI + Speech Recognition + Google Maps.  
    """
)

# --- Language Selection ---
lang = st.sidebar.selectbox("🌐 Choose Speaking Language:", ["English", "Hindi", "Bengali"], index=0)
lang_codes = {"English": "en", "Hindi": "hi", "Bengali": "bn"}

# --- Live Health News ---
st.sidebar.markdown("### 📰 Latest Health News")
news_loaded = False
fallback_news = [
    "WHO: Stay safe from seasonal flu",
    "New health guidelines released by Ministry of Health",
    "Experts recommend daily exercise for immunity"
]


API_KEY = "2dcbd656f7164c3c439a5b58c95cd0e5"
try:
    url = f"http://api.mediastack.com/v1/news?access_key={API_KEY}&categories=health&languages=en&countries=in&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        for article in news_data.get("data", [])[:5]:
            st.sidebar.markdown(f"🔹 [{article['title']}]({article['url']})")
    else:
        st.sidebar.markdown("⚠️ Could not fetch Mediastack news.")
except Exception as e:
    st.sidebar.markdown("⚠️ Error fetching Mediastack news.")

except:
    pass

if not news_loaded:
    try:
        rss_url = "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
        rss_data = requests.get(rss_url)
        root = ET.fromstring(rss_data.content)
        items = root.findall(".//item")
        if items:
            st.sidebar.markdown("🔄 Showing WHO Health Updates")
            for item in items[:3]:
                st.sidebar.markdown(f"🔹 [{item.find('title').text}]({item.find('link').text})")
            news_loaded = True
    except:
        pass

if not news_loaded:
    st.sidebar.markdown("⚠️ Attention News:")
    for item in fallback_news:
        st.sidebar.markdown(f"🔹 {item}")

st.sidebar.markdown("---")
st.sidebar.subheader("📢 Project Credits")
st.sidebar.markdown("**Team:** APPIFY US  \n**Hackathon:** ABC 2026  \n**Built with:** Python + Streamlit")

# --- Theme Selection ---
theme = st.sidebar.radio("🌓 Choose Theme:", ["🌞 Light Mode", "🌙 Dark Mode"], horizontal=True)

if theme == "🌙 Dark Mode":
    bg_color = "#1E1E1E"
    text_color = "#F5F5F5"
    card_color = "#2C2C2C"
    button_color = "#3B82F6"
    button_hover = "#2563EB"
else:  # Light mode
    bg_color = "#FFFFFF"
    text_color = "#212529"
    card_color = "#F8F9FA"
    button_color = "#3B82F6"
    button_hover = "#2563EB"


# Sidebar Health Summary
st.sidebar.markdown(
    """
    <style>
    .health-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 18px;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease-in-out;
    }
    .health-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 25px rgba(0,242,254,0.5);
    }
    .health-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 6px;
        text-shadow: 0px 0px 12px rgba(0,242,254,0.8);
    }
    .health-label {
        font-size: 1rem;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
/* Force sidebar to allow scrolling */
[data-testid="stSidebar"] {
    overflow-y: auto !important;
    max-height: 100vh;
}
</style>
""", unsafe_allow_html=True)
# --- Custom Styling ---

# --- Enhanced Custom Styling ---

# --- Full Visual Overhaul ---
st.markdown(f"""
<link href='https://fonts.googleapis.com/css?family=Montserrat:700,400|Roboto:400,500&display=swap' rel='stylesheet'>
<style>
.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -1;
    background:
        linear-gradient(120deg, #111 0%, #222 100% 60%),
        url('https://img.freepik.com/free-photo/medical-banner-background_23-2149613299.jpg?auto=format&fit=crop&w=1200&q=80') center center/cover no-repeat;
    background-blend-mode: darken, normal;
    opacity: 0.32;
}}
body {{
    min-height: 100vh;
    color: {text_color};
    font-family: 'Montserrat', 'Roboto', 'Segoe UI', Arial, sans-serif;
    transition: background 0.3s, color 0.3s;
}}
.main {{ padding: 32px; }}
/* Ensure main content is not hidden behind navbar */
.main, .block-container {{
     padding-top: 74px !important;
}}
h1, h2, h3 {{ font-family: 'Montserrat', sans-serif; font-weight: 700; color: {text_color}; }}
h1 {{
    text-align: center;
    font-size: 3rem;
    background: linear-gradient(270deg, #2563eb, #06b6d4, #2563eb);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 28px;
    letter-spacing: 1.5px;
    animation: gradientMove 3s ease-in-out infinite, fadeInDown 1.2s;
}}
body.light-mode {{
    background: linear-gradient(120deg, #e0e7ff 0%, #f8fafc 100%), url('https://www.transparenttextures.com/patterns/cubes.png');
    background-size: cover;
}}
body.dark-mode {{
    background: linear-gradient(120deg, #1E1E1E 0%, #23272f 100%);
    background-size: cover;
}}
@keyframes gradientMove {{
    0% {{background-position:0% 50%;}}
    50% {{background-position:100% 50%;}}
    100% {{background-position:0% 50%;}}
}}
@keyframes fadeInDown {{
    0% {{ opacity: 0; transform: translateY(-40px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes logo-bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-12px); }}
}}
.glass-card, .highlight-box {{
    position: relative;
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(16px);
    border-radius: 22px;
    box-shadow: 0 10px 36px rgba(60,130,246,0.13), 0 1.5px 8px rgba(6,182,212,0.09);
    padding: 22px 28px;
    margin-bottom: 26px;
    border: 2.5px solid;
    border-image: linear-gradient(120deg, #2563eb 10%, #06b6d4 90%) 1;
    transition: box-shadow 0.3s, transform 0.3s;
    animation: fadeInUp 1.1s;
    overflow: hidden;
}}
/* Sparkle animation for highlight boxes */
.highlight-box::before {{
    content: '';
    position: absolute;
    top: 18px; right: 18px;
    width: 18px; height: 18px;
    background: radial-gradient(circle, #fff 60%, #06b6d4 100%);
    border-radius: 50%;
    opacity: 0.7;
    animation: sparkleMove 2.8s infinite linear;
    pointer-events: none;
    z-index: 2;
}}
.highlight-box::after {{
    content: '';
    position: absolute;
    bottom: 14px; left: 22px;
    width: 12px; height: 12px;
    background: radial-gradient(circle, #2563eb 60%, #06b6d4 100%);
    border-radius: 50%;
    opacity: 0.5;
    animation: sparkleMove 3.5s infinite linear reverse;
    pointer-events: none;
    z-index: 2;
}}
@keyframes sparkleMove {{
    0% {{ transform: scale(1) translateY(0); opacity: 0.7; }}
    50% {{ transform: scale(1.2) translateY(-10px); opacity: 1; }}
    100% {{ transform: scale(1) translateY(0); opacity: 0.7; }}
}}
/* Inner glow */
.highlight-box {{
    box-shadow: 0 0 0 8px rgba(37,99,235,0.04) inset, 0 10px 36px rgba(60,130,246,0.13), 0 1.5px 8px rgba(6,182,212,0.09);
}}
.highlight-box:hover, .glass-card:hover {{
    box-shadow: 0 16px 48px rgba(60,130,246,0.18);
    transform: translateY(-2px) scale(1.02);
}}
@keyframes fadeInUp {{
    0% {{ opacity: 0; transform: translateY(40px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}
.stButton>button {{
    background: linear-gradient(90deg, #3b82f6 60%, #06b6d4 100%);
    color: #fff;
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 16px;
    padding: 16px 36px;
    font-size: 18px;
    box-shadow: 0 4px 16px rgba(60,130,246,0.12);
    transition: all 0.3s;
    letter-spacing: 0.5px;
    animation: fadeInUp 1.2s;
}}
.stButton>button:hover {{
    background: linear-gradient(90deg, #2563eb 60%, #06b6d4 100%);
    transform: scale(1.08);
    box-shadow: 0 8px 32px rgba(60,130,246,0.18);
}}
.stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
    border-radius: 18px !important;
    border: 2.5px solid !important;
    border-image: linear-gradient(120deg, #2563eb 10%, #06b6d4 90%) 1 !important;
    padding: 14px 16px !important;
    background: rgba(255,255,255,0.85) !important;
    color: {text_color} !important;
    font-size: 18px !important;
    box-shadow: 0 4px 18px rgba(60,130,246,0.10), 0 1.5px 8px rgba(6,182,212,0.09);
    animation: fadeInUp 1.3s;
    transition: border-color 0.3s, box-shadow 0.3s;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
    border-color: #3b82f6 !important;
    outline: none !important;
}}
.stAlert {{
    border-radius: 16px !important;
    box-shadow: 0 2px 12px rgba(60,130,246,0.10);
}}
#chatbot-btn, .chat-btn {{
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    background: linear-gradient(135deg, #3b82f6, #06b6d4);
    color: white;
    border-radius: 50%;
    width: 68px;
    height: 68px;
    font-size: 34px;
    border: none;
    cursor: pointer;
    box-shadow: 0 8px 24px rgba(60,130,246,0.18);
    transition: all 0.3s;
    animation: fadeInUp 1.4s;
}}
#chatbot-btn:hover, .chat-btn:hover {{
    transform: scale(1.14);
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    box-shadow: 0 12px 40px rgba(60,130,246,0.22);
}}
.footer {{
    width: 100%;
    text-align: center;
    padding: 24px 0 12px 0;
    font-size: 1.1rem;
    color: #2563eb;
    background: transparent;
    border-top: none;
    margin-top: 0;
    font-family: 'Roboto', sans-serif;
}}
.footer a {{ color: #06b6d4; text-decoration: none; margin: 0 8px; font-weight: 500; }}
.footer a:hover {{ text-decoration: underline; }}
</style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown("""
<a id="home"></a>
<div style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:56px 0 40px 0;background:linear-gradient(120deg,rgba(37,99,235,0.12) 0%,rgba(6,182,212,0.12) 100%);border-radius:40px;box-shadow:0 12px 48px rgba(60,130,246,0.16);margin-bottom:0;overflow:hidden;margin-top:74px;">
    <style>
    html {{ scroll-behavior: smooth; }}
    .sparkle {{
        position: absolute;
        width: 18px; height: 18px;
        background: radial-gradient(circle, #fff 60%, #06b6d4 100%);
        border-radius: 50%;
        opacity: 0.7;
        animation: sparkleMove 3s infinite linear;
        pointer-events: none;
        z-index: 2;
    }}
    @keyframes sparkleMove {{
        0% {{ transform: translateY(0) scale(1); opacity: 0.7; }}
        50% {{ transform: translateY(-24px) scale(1.2); opacity: 1; }}
        100% {{ transform: translateY(0) scale(1); opacity: 0.7; }}
    }}
    .floating-icon {{
        position: absolute;
        width: 32px; height: 32px;
        opacity: 0.8;
        animation: floatIcon 4s infinite ease-in-out;
        z-index: 2;
    }}
    @keyframes floatIcon {{
        0% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-18px) scale(1.1); }}
        100% {{ transform: translateY(0); }}
    }}
    </style>
    <div class='sparkle' style='top:38px;left:18%;animation-delay:0s;'></div>
    <div class='sparkle' style='top:62px;right:16%;animation-delay:1.2s;'></div>
    <div class='sparkle' style='top:110px;left:32%;animation-delay=2.1s;'></div>
    <div style='position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;'>
        <svg viewBox="0 0 1440 320" style="position:absolute;top:-40px;left:0;width:100%;height:180px;">
            <defs>
                <linearGradient id="waveGradient" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#2563eb"/>
                    <stop offset="100%" stop-color="#06b6d4"/>
                </linearGradient>
            </defs>
            <path fill="url(#waveGradient)" fill-opacity="0.25" d="M0,160L60,149.3C120,139,240,117,360,128C480,139,600,181,720,186.7C840,192,960,160,1080,154.7C1200,149,1320,171,1380,181.3L1440,192L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z"></path>
        </svg>
    </div>
    <img src='https://img.icons8.com/ios-filled/90/4a90e2/doctor-male.png' alt='AI Health Logo' style='width:100px;animation:logo-bounce 2s infinite;margin-bottom:22px;box-shadow:0 6px 24px rgba(60,130,246,0.18);filter:drop-shadow(0 0 12px #06b6d4);z-index:1;'>
    <h1 style='margin-bottom:0;font-size:3.2rem;font-weight:900;letter-spacing:2px;background:linear-gradient(270deg,#2563eb,#06b6d4,#2563eb);background-size:600% 600%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:gradientMove 3s ease-in-out infinite,fadeInDown 1.2s;text-shadow:0 4px 24px rgba(6,182,212,0.18);z-index:1;'>
        <span style="display:inline-block;animation:glow 2s infinite alternate;">🏥</span> AI Health Assistant
    </h1>
    <span style='font-size:1.35rem;font-weight:600;color:#2563eb;margin-bottom:0;text-shadow:0 2px 12px rgba(60,130,246,0.14);z-index:1;'>Your Smart Medical Companion</span>
    <div style='margin-top:22px;font-size:1.12rem;color:#64748b;font-weight:400;z-index:1;'>
        <span style='background:rgba(255,255,255,0.8);padding:8px 22px;border-radius:18px;box-shadow:0 2px 12px rgba(60,130,246,0.10);font-size:1.08rem;'>
            <span style='margin-right:8px;vertical-align:middle;'><img src='https://img.icons8.com/color/32/artificial-intelligence.png' style='vertical-align:middle;filter:drop-shadow(0 0 6px #2563eb);'></span>
            Powered by <b>AI</b>, <b>Speech Recognition</b>, and <b>Google Maps</b>
        </span>
    </div>
    <a href='#symptom-input' style='margin-top:28px;display:inline-block;padding:16px 38px;font-size:1.18rem;font-weight:700;color:#fff;background:linear-gradient(90deg,#2563eb,#06b6d4);border-radius:18px;box-shadow:0 6px 24px rgba(60,130,246,0.18);text-decoration:none;letter-spacing:1px;transition:all 0.3s;animation:fadeInUp 1.3s;z-index:1;'>Get Started 🚀</a>
    <style>
    @keyframes glow {
        0% { filter: drop-shadow(0 0 0px #06b6d4); }
        100% { filter: drop-shadow(0 0 18px #06b6d4); }
    }
    </style>
</div>
""", unsafe_allow_html=True)


# --- Mood Selection ---
st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
mood = st.radio("😷 How are you feeling?", ["😊 Fine", "🤒 Sick", "😴 Tired", "🥵 Feverish", "🤧 Cough/Cold"], horizontal=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Location ---
st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
location = st.selectbox("📍 Select Your Location:", ["Village", "Kolkata", "Delhi", "Mumbai","Channai","Bangalore","Hydrabad","Pune","Locknow","Other"], index=0)
st.markdown("</div>", unsafe_allow_html=True)

# --- State ---
if "user_symptoms" not in st.session_state:
    st.session_state.user_symptoms = ""
if "history" not in st.session_state:
    st.session_state.history = []

# --- Analysis Function ---
def analyze_and_display():
    result = analyze_symptoms(st.session_state.user_symptoms + " " + location)
    illness = result.get("illness", "No illness detected.")
    health_center = result.get("health_center", "No center found.")

    # Illness & Health Center
    st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
    st.markdown("### 🩺 Possible Illness")
    st.success(f"**{illness}**")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
    st.markdown("### 🏥 Nearest Health Center")
    st.info(f"**{health_center}**")
    maps_query = urllib.parse.quote_plus(health_center + " " + location)
    # Embedded Map
    components.html(f"""
        <iframe width="100%" height="250" src="https://www.google.com/maps?q={maps_query}&output=embed"></iframe>
        """, height=260)
    st.markdown("</div>", unsafe_allow_html=True)

    # Health Tips
    st.markdown("<div class='health-tips'>", unsafe_allow_html=True)
    st.markdown("### 💡 Health Tips")
    tips = []
    if "fever" in illness.lower() or "🥵" in mood:
        tips += ["💧 Drink plenty of fluids", "🛌 Take rest", "🌡️ Monitor temperature regularly"]
    if "cold" in illness.lower() or "🤧" in mood:
        tips += ["☕ Drink warm water", "🌫️ Use steam inhalation", "❄️ Avoid cold drinks"]
    if "😴" in mood:
        tips += ["💤 Take a short nap", "🍎 Eat energy-rich snacks", "💧 Stay hydrated"]
    if not tips:
        tips = ["💧 Maintain proper hydration", "🥗 Eat balanced meals", "🧑‍⚕️ Consult a doctor if symptoms persist"]
    for tip in tips:
        st.markdown(f"- {tip}")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- TTS in selected language or detected ---
    try:
        detected_lang = detect(st.session_state.user_symptoms)
        tts_lang = detected_lang if detected_lang in ["en","hi","bn"] else lang_codes[lang]
        tts_text = f"Possible illness: {illness}. Nearest health center: {health_center}."
        tts = gTTS(text=tts_text, lang=tts_lang)
        audio_file = "tts_audio.mp3"
        tts.save(audio_file)
        st.audio(audio_file, format="audio/mp3")
    except:
        st.warning("⚠️ TTS failed. Showing text only.")

    # --- Add to history ---
    st.session_state.history.append(st.session_state.user_symptoms)

# --- Animated Anchor for Input Section ---
st.markdown("<a id='symptom-input'></a>", unsafe_allow_html=True)
# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
    st.session_state.user_symptoms = st.text_area("✍️ Type Your Symptoms Here:", value=st.session_state.user_symptoms, placeholder="e.g. fever, cough...")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
    recognizer = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    selected_mic_index = 0
    if len(mic_list) > 1:
        selected_mic_name = st.selectbox("🎤 Select Microphone:", mic_list)
        selected_mic_index = mic_list.index(selected_mic_name)
    else:
        st.info(f"🎤 Using default microphone: {mic_list[0]}")

    if st.button("🎙️ Record Voice"):
        st.info("🎙️ Listening... Speak clearly now.")
        with sr.Microphone(device_index=selected_mic_index) as source:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, phrase_time_limit=10)
                st.info("Processing speech...")
                text = recognizer.recognize_google(audio)
                st.success(f"✅ Recognized Speech: {text}")
                st.session_state.user_symptoms = text

                # Auto-analyze
                with st.spinner("🔎 AI is analyzing your symptoms..."):
                    time.sleep(1.5)
                    analyze_and_display()

            except sr.UnknownValueError:
                st.error("❌ Could not understand speech.")
            except sr.RequestError:
                st.error("⚠️ Speech service unavailable.")
    st.markdown("</div>", unsafe_allow_html=True)



# --- Manual Analyze Button ---
if st.button("🔍 Analyze Symptoms"):
    if st.session_state.user_symptoms.strip():
        with st.spinner("🔎 AI is analyzing your symptoms..."):
            time.sleep(1.5)
            analyze_and_display()
    else:
        st.warning("⚠️ Please enter or record symptoms first.")

# --- Show History & Copy ---

# --- Show History & Copy ---
if st.session_state.history:
    st.markdown("<div class='highlight-box history-list'>", unsafe_allow_html=True)
    st.markdown("### 🕘 Previous Inputs")
    for h in st.session_state.history[-5:][::-1]:
        st.markdown(f"<span style='color:#2563eb;font-weight:500;'>• {h}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("📋 Copy Symptoms"):
    pyperclip.copy(st.session_state.user_symptoms)
    st.success("Copied to clipboard!")

# --- CHATBOT FEATURE ---

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ai_typing" not in st.session_state:
    st.session_state.ai_typing = False

# Chat section starts here


# =====================
# Health Monitor Section (Rings + Charts)
# =====================
st.markdown("<a id='health'></a>", unsafe_allow_html=True)
st.markdown('<div class="health-title">📊 Health Monitor</div>', unsafe_allow_html=True)

import matplotlib.pyplot as plt

# Simulated history storage
if "vital_history" not in st.session_state:
    st.session_state.vital_history = {"heart": [], "spo2": [], "temp": [], "bp_sys": [], "bp_dia": []}

# Inputs
heart_rate = st.number_input("❤️ Heart Rate (bpm)", 30, 200, 75)
spo2 = st.number_input("🫁 Oxygen Saturation (%)", 50, 100, 98)
temperature = st.number_input("🌡️ Temperature (°C)", 30.0, 45.0, 36.6, step=0.1)
bp_systolic = st.number_input("🩸 BP Systolic (mmHg)", 80, 200, 120)
bp_diastolic = st.number_input("🩸 BP Diastolic (mmHg)", 50, 120, 80)

# Save history
st.session_state.vital_history["heart"].append(heart_rate)
st.session_state.vital_history["spo2"].append(spo2)
st.session_state.vital_history["temp"].append(temperature)
st.session_state.vital_history["bp_sys"].append(bp_systolic)
st.session_state.vital_history["bp_dia"].append(bp_diastolic)

# =====================
# Progress Rings (Current Values)
# =====================
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="progress-ring" style="--percent:{(heart_rate/200)*100}; --color:red;">
            <div class="progress-value">{heart_rate} bpm</div>
        </div>
        <p style="text-align:center;">❤️ Heart Rate</p>
        """, unsafe_allow_html=True)

with col2:
    st.markdown(
        f"""
        <div class="progress-ring" style="--percent:{spo2/100}; --color:blue;">
            <div class="progress-value">{spo2}%</div>
        </div>
        <p style="text-align:center;">🫁 SpO₂</p>
        """, unsafe_allow_html=True)

with col3:
    st.markdown(
        f"""
        <div class="progress-ring" style="--percent:{temperature/45}; --color:orange;">
            <div class="progress-value">{temperature} °C</div>
        </div>
        <p style="text-align:center;">🌡️ Temperature</p>
        """, unsafe_allow_html=True)

col4, col5 = st.columns(2)
with col4:
    st.markdown(
        f"""
        <div class="progress-ring" style="--percent:{bp_systolic/200}; --color:green;">
            <div class="progress-value">{bp_systolic}</div>
        </div>
        <p style="text-align:center;">🩸 BP Systolic</p>
        """, unsafe_allow_html=True)
with col5:
    st.markdown(
        f"""
        <div class="progress-ring" style="--percent:{bp_diastolic/120}; --color:purple;">
            <div class="progress-value">{bp_diastolic}</div>
        </div>
        <p style="text-align:center;">🩸 BP Diastolic</p>
        """, unsafe_allow_html=True)

# =====================
# Alerts
# =====================
st.subheader("⚠️ Health Alerts")
if heart_rate < 60 or heart_rate > 100:
    st.error("Abnormal Heart Rate detected!")
if spo2 < 95:
    st.error("Low Oxygen Saturation detected!")
if temperature < 36.1 or temperature > 37.5:
    st.error("Abnormal Body Temperature detected!")
if bp_systolic > 140:
    st.error("High Systolic BP detected!")
if bp_diastolic > 90:
    st.error("High Diastolic BP detected!")
if bp_systolic < 90:
    st.error("Low Systolic BP detected!")
if bp_diastolic < 60:
    st.error("Low Diastolic BP detected!")
else:
    st.success("All vitals are within normal range ✅")

# =====================
# Live Charts (History)
# =====================
st.subheader("📈 Live Health Trends")

def plot_vital(values, label, color, icon):
    """Plot vital signs with enhanced visual styling"""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')
    
    # Plot with gradient effect
    ax.plot(values, marker="o", linestyle="-", color=color, linewidth=3.5, 
            markersize=8, label=label, markerfacecolor=color, markeredgewidth=2, 
            markeredgecolor='white', alpha=0.95)
    
    # Enhanced styling
    ax.set_title(f"{icon} {label}", fontsize=16, fontweight='bold', 
                color='#58a6ff', pad=20)
    ax.set_ylabel(label, fontsize=12, fontweight='bold', color='#c9d1d9')
    ax.set_xlabel("Timeline", fontsize=12, fontweight='bold', color='#c9d1d9')
    
    # Grid styling
    ax.grid(True, alpha=0.2, linestyle='--', color='#30363d', linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Spine styling
    for spine in ax.spines.values():
        spine.set_color('#30363d')
        spine.set_linewidth(1.5)
    
    # Tick styling
    ax.tick_params(colors='#c9d1d9', labelsize=11, length=6, width=1.5)
    
    # Add gradient background effect
    ax.fill_between(range(len(values)), values, alpha=0.15, color=color)
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if len(st.session_state.vital_history["heart"]) > 1:
        plot_vital(st.session_state.vital_history["heart"], "Heart Rate (bpm)", "#FF6B6B", "❤️")
    if len(st.session_state.vital_history["spo2"]) > 1:
        plot_vital(st.session_state.vital_history["spo2"], "Oxygen Saturation (%)", "#4ECDC4", "🫁")

with chart_col2:
    if len(st.session_state.vital_history["temp"]) > 1:
        plot_vital(st.session_state.vital_history["temp"], "Temperature (°C)", "#FFD93D", "🌡️")
    if len(st.session_state.vital_history["bp_sys"]) > 1:
        bp_col1, bp_col2 = st.columns(2)
        with bp_col1:
            if len(st.session_state.vital_history["bp_sys"]) > 1:
                plot_vital(st.session_state.vital_history["bp_sys"], "BP Systolic (mmHg)", "#6BCB77", "💪")
        with bp_col2:
            if len(st.session_state.vital_history["bp_dia"]) > 1:
                plot_vital(st.session_state.vital_history["bp_dia"], "BP Diastolic (mmHg)", "#A8E6CF", "🩹")

st.markdown('</div>', unsafe_allow_html=True)

max_len = 20
st.session_state.vital_history["heart"] = st.session_state.vital_history["heart"][-max_len:]


# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="AIDOC - AI Health Assistant", page_icon="🧠", layout="wide")

# ------------------- THEME COLORS -------------------
BG = "#111312"
NEON_GREEN = "#00FF9C"
NEON_CYAN = "#00E5FF"
CARD = "#101717"
TEXT = "#E0FFF9"

# ------------------- CUSTOM CSS -------------------
st.markdown(f"""
    <style>
    body {{
        background-color: {BG};
        color: {TEXT};
        font-family: 'Poppins', sans-serif;
    }}
    h1, h2, h3, h4 {{
        text-align: center;
        color: {NEON_CYAN};
        text-shadow: 0 0 10px {NEON_CYAN};
    }}
    .glass-card {{
        background: rgba(20,30,25,0.8);
        border: 1px solid rgba(0,255,180,0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0,255,180,0.2);
        animation: fadeIn 1s ease-in-out;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, {NEON_GREEN}, {NEON_CYAN});
        color: black;
        border: none;
        border-radius: 12px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 0 12px {NEON_CYAN};
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 22px {NEON_GREEN};
    }}
    .health-tips {{
        background: rgba(0,255,180,0.1);
        border-left: 5px solid {NEON_CYAN};
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: {TEXT};
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
""", unsafe_allow_html=True)



# ------------------- SMART DAILY TIPS -------------------
health_tips = [
    "💧 Stay hydrated – aim for 8 glasses of water daily!",
    "🍎 Add one fruit to your breakfast every day.",
    "🧘 Take a 2-minute mindfulness break every hour.",
    "🚶‍♂️ Walk at least 5,000 steps daily for better metabolism.",
    "💤 Sleep 7–8 hours to boost recovery and mood.",
]
tip = random.choice(health_tips)
st.markdown(f"<div class='health-tips'>{tip}</div>", unsafe_allow_html=True)

# ------------------- HEALTH DASHBOARD -------------------
st.subheader("📊 Health Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, step=0.5)
with col2:
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.5)
with col3:
    sleep = st.slider("Sleep Duration (hrs)", 0, 12, 7)

if height > 0:
    bmi = round(weight / ((height/100)**2), 2)
    st.success(f"**Your BMI:** {bmi}")

if bmi < 18.5:
    st.info("🟡 You are underweight.")
elif 18.5 <= bmi < 25:
    st.success("🟢 You are in the healthy range!")
elif 25 <= bmi < 30:
    st.warning("🟠 You are overweight.")
else:
    st.error("🔴 You are obese.")

hydration = round(weight * 0.035, 1)
st.markdown(f"💧 **Recommended Water Intake:** {hydration} liters/day")



# ------------------- PDF DOWNLOAD -------------------
st.subheader("📥 Download Health Report")

if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()

    # Use built-in font
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "AIDOC Health Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Date: {datetime.date.today()}", ln=True)
    pdf.cell(200, 10, f"BMI: {bmi}", ln=True)
    pdf.cell(200, 10, f"Recommended Water Intake: {hydration} L/day", ln=True)
    pdf.cell(200, 10, f"Sleep Duration: {sleep} hours", ln=True)

    # Remove unsupported characters (like emojis) from tip
    safe_tip = tip.encode("latin-1", "ignore").decode("latin-1")
    pdf.cell(200, 10, f"Health Tip: {safe_tip}", ln=True)

    file_path = "AIDOC_Report.pdf"
    pdf.output(file_path)
    with open(file_path, "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name=file_path, mime="application/pdf")

import streamlit as st
import time

# Initialize session state
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ai_typing" not in st.session_state:
    st.session_state.ai_typing = False
if "symptom_context" not in st.session_state:
    st.session_state.symptom_context = []

# Anchor and toggle button
st.markdown("<a id='chat'></a>", unsafe_allow_html=True)
toggle = st.button("💬 Open Chatbot", key="ChatbotToggle", help="Click to open chatbot")

if toggle:
    st.session_state.chat_open = not st.session_state.chat_open

# Chatbot UI
if st.session_state.chat_open:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🤖 AI Health Chatbot")
    st.info("⚠️ This chatbot provides general health guidance and is not a substitute for professional medical advice.")

    # Display chat history
    for i, entry in enumerate(st.session_state.chat_history):
        st.markdown(f"<div style='background:#eef;padding:10px;border-radius:10px;margin-bottom:5px'><strong>🧑 You:</strong> {entry['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#f9f9f9;padding:10px;border-radius:10px;margin-bottom:10px'><strong>🤖 AI:</strong> {entry['bot']}</div>", unsafe_allow_html=True)

        # Feedback
        if "feedback" not in entry:
            feedback = st.radio("Was this helpful?", ["👍 Yes", "👎 No"], key=f"feedback_{i}")
            st.session_state.chat_history[i]["feedback"] = feedback

    # AI typing simulation
    if st.session_state.ai_typing:
        with st.spinner("🤖 AI is typing..."):
            time.sleep(1.5)
            st.session_state.ai_typing = False
            st.rerun()

    # Chat input
    user_message = st.text_input("💬 Type your message:")
    if st.button("Send", key="chat_send"):
        if user_message.strip():
            st.session_state.chat_history.append({"user": user_message, "bot": "..."})
            st.session_state.symptom_context.append(user_message)
            st.session_state.ai_typing = True
            st.rerun()

    # Simple local symptom analyzer
    def analyze_symptoms(message):
        message = message.lower()
        if "fever" in message and "cough" in message:
            return {"illness": "You may have symptoms of flu or a viral infection. Stay hydrated and rest."}
        elif "headache" in message and "nausea" in message:
            return {"illness": "These symptoms could indicate a migraine or dehydration. Consider resting in a dark room."}
        elif "sore throat" in message:
            return {"illness": "A sore throat might be due to a cold or mild infection. Gargling warm salt water may help."}
        elif "stomach pain" in message or "diarrhea" in message:
            return {"illness": "You may be experiencing a digestive issue. Avoid spicy food and drink plenty of fluids."}
        else:
            return {"illness": "I'm here to help! Please describe your symptoms in more detail."}

    # Generate AI response
    if not st.session_state.ai_typing and st.session_state.chat_history and st.session_state.chat_history[-1]['bot'] == "...":
        result = analyze_symptoms(st.session_state.chat_history[-1]['user'])
        reply = result.get("illness", "I'm here to help you stay healthy!")
        st.session_state.chat_history[-1]['bot'] = reply
        st.rerun()

    # Auto-scroll
    st.markdown("<script>window.scrollTo(0,document.body.scrollHeight);</script>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
import datetime
import random

# --- Daily Health Tips ---
daily_tips = [
    "💧 Stay hydrated! Drink at least 8 glasses of water today.",
    "🚶 Take a short 10-minute walk every few hours.",
    "🍎 Add one fruit to your meal today for better digestion.",
    "🧘 Take 5 deep breaths and relax your mind for a moment.",
    "💤 Make sure to sleep at least 7 hours tonight.",
    "☀️ Get some sunlight — Vitamin D boosts your mood!",
    "❤️ Check your posture! Sit straight and stretch your back.",
    "🍋 Start your day with a glass of warm lemon water.",
    "🏃 Do 20 squats or a quick cardio burst — feel energized!",
    "📵 Take a 15-minute screen break for your eyes."
]

# Pick one per day based on date
today = datetime.date.today()
tip_index = today.day % len(daily_tips)
daily_tip = daily_tips[tip_index]

# --- Display Notification ---
st.markdown(f"""
<div style="
    background: linear-gradient(90deg, #00ffcc33, #00ffff33);
    border: 1.5px solid #00ffff99;
    color: #00ffe1;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 500;
    margin-top: 15px;
    box-shadow: 0 0 12px rgba(0,255,200,0.25);
    animation: fadeIn 1s ease-in-out;
">
🧠 <b>Daily Health Tip:</b><br>{daily_tip}
</div>
""", unsafe_allow_html=True)
# pip install plyer
from plyer import notification
from twilio.rest import Client

notification.notify(
    title="💡 AIDOC Health Reminder",
    message=daily_tip,
    timeout=10
)

st.markdown("<h2>📱 Subscribe for Daily Health SMS</h2>", unsafe_allow_html=True)
phone_file = "subscribers.csv"

if os.path.exists(phone_file):
    subscribers = pd.read_csv(phone_file)
else:
    subscribers = pd.DataFrame(columns=["phone"])

# Initialize session state for phone input
if "phone_input" not in st.session_state:
    st.session_state.phone_input = ""

phone = st.text_input("Enter your phone number (with country code)", placeholder="+91XXXXXXXXXX", key="phone_input")

if st.button("✅ Subscribe"):
    phone = st.session_state.phone_input.strip()
    if phone:
        if phone not in subscribers["phone"].values:
            new_entry = pd.DataFrame([[phone]], columns=["phone"])
            subscribers = pd.concat([subscribers, new_entry], ignore_index=True)
            subscribers.to_csv(phone_file, index=False)
            st.success("🎉 You’re now subscribed to AIDOC Daily Health Tips!")
        else:
            st.info("📬 You’re already subscribed.")
    else:
        st.warning("⚠️ Please enter a valid number.")

# ------------------ SEND SMS (Admin only) ------------------


# ------------------ FLOATING CHATBOT BUTTON ------------------
st.markdown("""
<button id="chatbot-btn" onclick="alert('🤖 AIDOC Chatbot coming soon!')">💬</button>
""", unsafe_allow_html=True)



# ------------------- FOOTER -------------------
st.markdown(f"""
<hr style='border:1px solid {NEON_CYAN};opacity:0.3;'>
<div style='text-align:center;color:{NEON_GREEN};'>
    <b>💡 AIDOC © 2025 | Powered by AI & Love for Health</b>
</div>
""", unsafe_allow_html=True)
# --- Footer ---
st.markdown("""
<div class='footer'>
    <span>Made with ❤️ by <b>OPTIMUS BYTE</b> | Hackathon: TECHNOLOGIA 2025</span><br>
    <span>Built with <b>Python</b> + <b>Streamlit</b></span><br>
    <a href='https://github.com/' target='_blank'>GitHub</a> · <a href='https://streamlit.io/' target='_blank'>Streamlit</a> · <a href='https://icons8.com/' target='_blank'>Icons8</a>
    <br><span style='font-size:0.95rem;color:#94a3b8;'>© 2025 AI Health Assistant. All rights reserved.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.chatbot-output {
    color: #111 !important;
    background: #fff;
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 1.1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

