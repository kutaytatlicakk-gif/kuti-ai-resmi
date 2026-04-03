import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- API VE SAYFA AYARLARI ---
st.set_page_config(page_title="KutiAI v17.0 PRO", page_icon="⚡", layout="wide")
API_KEY = "AIzaSyDrlWEmJ6haheLyVMDLvftNt7ZxQS26c1o" # Yeni anahtarın
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- KLASÖR AYARI ---
# Sohbetleri kaydetmek için bir klasör oluşturur
if not os.path.exists("chats"):
    os.makedirs("chats")

# --- SESSION STATE (HAFIZA) ---
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FONKSİYONLAR ---
def sohbeti_kaydet():
    if st.session_state.messages:
        file_path = f"chats/{st.session_state.current_chat_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False)

def sohbeti_yukle(chat_id):
    file_path = f"chats/{chat_id}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.session_state.messages = json.load(f)
            st.session_state.current_chat_id = chat_id

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    
    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True):
        sohbeti_kaydet() # Eskisini kaydet
        st.session_state.messages = [] # Ekranı temizle
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.markdown("---")
    st.subheader("🕒 Eski Sohbetlerin")
    
    # Kayıtlı dosyaları listele
    chat_files = sorted(os.listdir("chats"), reverse=True)
    for file in chat_files:
        chat_id = file.replace(".json", "")
        # Dosyanın içindeki ilk mesajı başlık olarak alalım
        try:
            with open(f"chats/{file}", "r", encoding="utf-8") as f:
                content = json.load(f)
                baslik = content[0]["content"][:25] + "..." if content else chat_id
        except:
            baslik = chat_id
            
        if st.button(f"💬 {baslik}", key=chat_id, use_container_width=True):
            sohbeti_yukle(chat_id)
            st.rerun()

# --- ANA SOHBET EKRANI ---
st.title("🤖 KutiAI Siber Asistan")
st.caption(f"Şu anki Oturum: {st.session_state.current_chat_id}")

# Mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
prompt = st.chat_input("Yusuf, bir şeyler yaz...")

if prompt:
    # 1. Kullanıcı mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI cevabı
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            ai_cevap = response.text
            st.markdown(ai_cevap)
            st.session_state.messages.append({"role": "assistant", "content": ai_cevap})
            sohbeti_kaydet() # Her cevapta otomatik kaydet
        except Exception as e:
            st.error(f"Hata: {e}")
