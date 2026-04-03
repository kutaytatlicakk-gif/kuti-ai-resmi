import streamlit as st
import google.generativeai as genai

# --- API AYARI ---
API_KEY = "AIzaSyAy4UAzQafV4GmwdNo_w6tS3dmzirD0P4Q"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- HAFIZA SİSTEMİ (En Başta Olmalı) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SAYFA BAŞLIĞI ---
st.title("🤖 KutiAI Siber Asistan")
st.write("Yusuf'un Özel Yapay Zekası")

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("Sistem Paneli")
    st.success("Durum: Aktif")
    
    # Sohbet Geçmişi Temizleme Butonu
    if st.button("Geçmişi Sil"):
        st.session_state.messages = []
        st.rerun()

# --- SOHBETİ EKRANA YAZDIRMA ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- KULLANICI GİRİŞİ ---
prompt = st.chat_input("Mesajınızı buraya yazın...")

if prompt:
    # 1. Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Yapay zeka cevabını al
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            ai_cevap = response.text
            st.write(ai_cevap)
            st.session_state.messages.append({"role": "assistant", "content": ai_cevap})
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
