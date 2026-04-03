import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- GEMINI YAPILANDIRMASI ---
API_KEY = "AIzaSyAy4UAzQafV4GmwdNo_w6tS3dmzirD0P4Q"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="KutiAI v15.0", page_icon="🤖", layout="wide")

# Hacker Teması İçin CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stStatusWidget { display:none; }
    .stChatFloatingInputContainer { background-color: #1a1a1a; }
    </style>
    """, unsafe_allow_state_html=True)

# --- HAFIZA SİSTEMİ (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    st.write("---")
    st.success("● SİSTEM: AKTİF")
    st.info("● MOD: STREAMLIT HAFIZA")
    
    st.subheader("📜 Sohbet Geçmişi")
    # Geçmiş mesajları kısa özet olarak göster
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.write(f"{i+1}. {msg['content'][:20]}...")

    st.write("---")
    if st.button("🗑️ GEÇMİŞİ SIFIRLA", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- ANA SOHBET EKRANI ---
st.title("Siber Asistan: KutiAI")

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Komutunuz nedir Yusuf?"):
    # Kullanıcı mesajını göster ve hafızaya ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini'den cevap al
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            # Yapay zeka cevabını hafızaya ekle
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Hata: {e}")
