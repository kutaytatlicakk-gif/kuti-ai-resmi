import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. AYARLAR VE GÜVENLİK ---
st.set_page_config(page_title="KutiAI PRO v17.5", page_icon="⚡", layout="wide")

# API Anahtarın
API_KEY = "AIzaSyDrlWEmJ6haheLyVMDLvftNt7ZxQS26c1o"
genai.configure(api_key=API_KEY)

# --- 2. HATA VERMEYEN MODEL BAĞLANTISI ---
@st.cache_resource
def model_bagla():
    # Hata veren 1.5-flash yerine daha stabil olan sürümü deniyoruz
    modeller = ["gemini-1.5-flash", "gemini-1.0-pro"]
    for m_adi in modeller:
        try:
            test_model = genai.GenerativeModel(m_adi)
            # Küçük bir test yapalım
            test_model.generate_content("test")
            return test_model
        except:
            continue
    return genai.GenerativeModel("gemini-pro")

model = model_bagla()

# --- 3. KLASÖR VE HAFIZA SİSTEMİ ---
if not os.path.exists("chats"):
    os.makedirs("chats")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- 4. SOHBET KAYIT FONKSİYONLARI ---
def sohbeti_kaydet():
    if st.session_state.messages:
        # Eğer bu yeni bir sohbetse ID oluştur
        if st.session_state.current_chat_id is None:
            st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        file_path = f"chats/{st.session_state.current_chat_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False)

def sohbeti_yukle(chat_id):
    file_path = f"chats/{chat_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        st.session_state.messages = json.load(f)
        st.session_state.current_chat_id = chat_id

# --- 5. YAN PANEL (CHATGPT TARZI LİSTE) ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    
    if st.button("➕ Yeni Sohbet", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()

    st.markdown("---")
    st.subheader("💬 Sohbetlerin")
    
    # Dosyaları tarihe göre listele
    files = sorted([f for f in os.listdir("chats") if f.endswith(".json")], reverse=True)
    
    for f in files:
        cid = f.replace(".json", "")
        # İlk mesajı başlık yap
        try:
            with open(f"chats/{f}", "r", encoding="utf-8") as file_data:
                chat_data = json.load(file_data)
                label = chat_data[0]["content"][:25] + "..." if chat_data else cid
        except:
            label = cid
            
        # Eğer şu anki sohbetse rengi farklı olsun (veya işaret koyalım)
        is_active = "▶ " if st.session_state.current_chat_id == cid else ""
        if st.button(f"{is_active}{label}", key=cid, use_container_width=True):
            sohbeti_yukle(cid)
            st.rerun()

# --- 6. ANA EKRAN ---
st.title("🤖 KutiAI Siber Asistan")

# Mesajları göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Giriş alanı
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Mesajı ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cevabı al
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            sohbeti_kaydet() # Kaydet
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
