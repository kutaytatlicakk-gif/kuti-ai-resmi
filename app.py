import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. SİSTEM AYARLARI ---
st.set_page_config(page_title="KutiAI PRO v18.0", page_icon="⚡", layout="wide")

# API Anahtarı
API_KEY = "AIzaSyDrlWEmJ6haheLyVMDLvftNt7ZxQS26c1o"
genai.configure(api_key=API_KEY)

# --- 2. KIRILMAZ MODEL MOTORU (404 HATASINA SON) ---
@st.cache_resource
def siber_model_bagla():
    # Google sunucularından anlık çalışan modellerin listesini çeker
    calisan_modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 1. Öncelik: En güncel ve hızlı olan Flash modelini bul
    for m_adi in calisan_modeller:
        if "flash" in m_adi:
            return genai.GenerativeModel(m_adi)
            
    # 2. Öncelik: Bulamazsa, çalışan listedeki ilk modeli al (Böylece asla 404 vermez)
    return genai.GenerativeModel(calisan_modeller[0])

# Asistanı canlı modele bağla
model = siber_model_bagla()

# --- 3. VERİTABANI (KLASÖR VE HAFIZA) ---
if not os.path.exists("chats"):
    os.makedirs("chats")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- 4. SOHBET KAYIT SİSTEMİ ---
def sohbeti_kaydet():
    if st.session_state.messages:
        if st.session_state.current_chat_id is None:
            st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        file_path = f"chats/{st.session_state.current_chat_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False)

def sohbeti_yukle(chat_id):
    file_path = f"chats/{chat_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.session_state.messages = json.load(f)
            st.session_state.current_chat_id = chat_id

# --- 5. YAN PANEL (PROFESYONEL LİSTE) ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    
    if st.button("➕ Yeni Sohbet", use_container_width=True):
        if st.session_state.messages:
            sohbeti_kaydet()
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Sohbet Geçmişi")
    
    # Kaydedilen sohbet dosyalarını bul ve listele
    files = sorted([f for f in os.listdir("chats") if f.endswith(".json")], reverse=True)
    
    for f in files:
        cid = f.replace(".json", "")
        # Başlık olarak sohbetin ilk mesajını al
        try:
            with open(f"chats/{f}", "r", encoding="utf-8") as file_data:
                chat_data = json.load(file_data)
                label = chat_data[0]["content"][:25] + "..." if chat_data else cid
        except:
            label = cid
            
        # Aktif sohbeti işaretle
        is_active = "▶ " if st.session_state.current_chat_id == cid else ""
        if st.button(f"{is_active}{label}", key=cid, use_container_width=True):
            sohbeti_yukle(cid)
            st.rerun()

# --- 6. ANA SOHBET EKRANI ---
st.title("🤖 KutiAI Siber Asistan")
st.caption("Kesintisiz Bağlantı | Oto-Model Seçimi Aktif")

# Hafızadaki mesajları ekrana bas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Yeni komut alma
if prompt := st.chat_input("Yusuf, sistem hazır. Komutunuz nedir?"):
    # Senin mesajın
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka cevabı
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            sohbeti_kaydet() # Konuşmayı anında yedekle
        except Exception as e:
            st.error(f"Sistem Hatası (Google API): {e}")
