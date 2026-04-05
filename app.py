import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- SİSTEM AYARLARI ---
st.set_page_config(page_title="KutiAI PRO v18.0", page_icon="⚡", layout="wide")

# API Anahtarı Kasadan Çekiliyor
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına API anahtarını ekle!")
    st.stop()

# Model Bağlantısı
model = genai.GenerativeModel('gemini-1.5-flash')

# Klasörleme Sistemi
if not os.path.exists("chats"):
    os.makedirs("chats")

# Hafıza Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- YAN PANEL (GEÇMİŞ LİSTESİ) ---
with st.sidebar:
    st.title("⚡ KutiAI Geçmişi")
    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()
    
    st.write("---")
    # Kayıtlı dosyaları listele (İstediğin sol liste burası)
    files = sorted([f for f in os.listdir("chats") if f.endswith(".json")], reverse=True)
    for f in files:
        cid = f.replace(".json", "")
        if st.button(f"💬 {cid[:13]}", key=cid, use_container_width=True):
            with open(f"chats/{f}", "r", encoding="utf-8") as f_in:
                st.session_state.messages = json.load(f_in)
                st.session_state.chat_id = cid
            st.rerun()

# --- ANA EKRAN ---
st.title("🤖 KutiAI Siber Asistan")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    
    with st.chat_message("assistant"):
        try:
            r = model.generate_content(p)
            st.markdown(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
            # Otomatik Kaydet
            with open(f"chats/{st.session_state.chat_id}.json", "w", encoding="utf-8") as f_out:
                json.dump(st.session_state.messages, f_out, ensure_ascii=False)
        except Exception as e:
            st.error(f"Hata: {e}")
