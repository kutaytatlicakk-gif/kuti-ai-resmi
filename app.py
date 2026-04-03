import streamlit as st
import google.generativeai as genai

# --- GEMINI YAPILANDIRMASI ---
# API Key'ini buraya yazdım
API_KEY = "AIzaSyAy4UAzQafV4GmwdNo_w6tS3dmzirD0P4Q"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="KutiAI v15.0", page_icon="🤖")

# --- HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    st.info("● SİSTEM: BULUTTA AKTİF")
    
    st.subheader("📜 Sohbet Özetleri")
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.write(f"{i+1}. {msg['content'][:20]}...")

    if st.button("🗑️ GEÇMİŞİ TEMİZLE"):
        st.session_state.messages = []
        st.rerun()

# --- ANA SOHBET EKRANI ---
st.title("KutiAI Siber Asistan")

# Eski mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Yusuf, bir komut gir..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
