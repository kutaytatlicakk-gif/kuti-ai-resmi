import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. SİSTEM AYARLARI ---
st.set_page_config(page_title="KutiAI PRO v19.0", page_icon="⚡", layout="wide")

# API Anahtarını Kasa (Secrets) Üzerinden Çek
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ API Anahtarı bulunamadı! Settings > Secrets kısmına GEMINI_API_KEY ekle.")
    st.stop()

# --- 2. OTOMATİK MODEL SEÇİCİ (HATA ÖNLEYİCİ) ---
@st.cache_resource
def dinamik_model_bagla():
    try:
        # Google'daki aktif modelleri listele
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Öncelik sırasına göre en stabil olanı seç
        for m_adi in modeller:
            if "gemini-1.5-flash" in m_adi: return genai.GenerativeModel(m_adi)
        for m_adi in modeller:
            if "gemini-pro" in m_adi: return genai.GenerativeModel(m_adi)
            
        # Hiçbiri yoksa listedeki ilkini al (Asla 404 vermez)
        return genai.GenerativeModel(modeller[0])
    except Exception as e:
        st.error(f"Sistem Modelleri Çekemedi: {e}")
        st.stop()

model = dinamik_model_bagla()

# --- 3. VERİ SİSTEMİ (KLASÖRLEME) ---
CHAT_DIR = "chats"
if not os.path.exists(CHAT_DIR):
    os.makedirs(CHAT_DIR)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 4. YAN PANEL (GEÇMİŞ LİSTESİ) ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    if st.button("➕ Yeni Sohbet", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.markdown("---")
    st.subheader("🕒 Sohbet Geçmişi")
    
    # Kayıtlı dosyaları listele
    files = sorted([f for f in os.listdir(CHAT_DIR) if f.endswith(".json")], reverse=True)
    for f in files:
        cid = f.replace(".json", "")
        # İlk mesajı başlık olarak göster
        try:
            with open(f"{CHAT_DIR}/{f}", "r", encoding="utf-8") as f_data:
                chat_data = json.load(f_data)
                label = chat_data[0]["content"][:20] + "..." if chat_data else cid
        except:
            label = cid
            
        if st.button(f"💬 {label}", key=cid, use_container_width=True):
            with open(f"{CHAT_DIR}/{f}", "r", encoding="utf-8") as f_in:
                st.session_state.messages = json.load(f_in)
                st.session_id = cid
            st.rerun()

# --- 5. ANA SOHBET EKRANI ---
st.title("🤖 KutiAI Siber Asistan")
st.caption(f"Aktif Model: {model.model_name}")

# Mesajları Ekrana Bas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Yusuf, emrindeyim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # Otomatik Kayıt
            with open(f"{CHAT_DIR}/{st.session_state.session_id}.json", "w", encoding="utf-8") as f_out:
                json.dump(st.session_state.messages, f_out, ensure_ascii=False)
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
