import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI (En başta olmalı) ---
st.set_page_config(page_title="KutiAI v15.0 PRO", page_icon="⚡", layout="wide")

# --- API VE MODEL AYARI (Kesin Çözüm Burası) ---
# Kendi API anahtarın
API_KEY = "AIzaSyAy4UAzQafV4GmwdNo_w6tS3dmzirD0P4Q"
genai.configure(api_key=API_KEY)

# Google'ın eski 'gemini-pro' modeli kapandığı için en güncel ve sorunsuz çalışan modeli tanımlıyoruz:
model = genai.GenerativeModel('gemini-1.5-flash')

# --- HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN PANEL (SIDEBAR) TASARIMI ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    st.success("Sistem Durumu: Çevrimiçi ve Stabil")
    st.info("Aktif Model: Gemini 1.5 Flash")
    
    st.markdown("---")
    
    # Hafıza Temizleme Butonu (Tüm genişliği kaplar)
    if st.button("🗑️ Sohbeti Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN TASARIMI ---
st.title("🤖 KutiAI Siber Asistan")
st.caption("Yusuf'un Özel Geliştirilmiş Yapay Zekası - Kesintisiz Bağlantı Aktif")
st.markdown("---")

# --- SOHBETİ EKRANA YAZDIRMA ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ VE İŞLEM ---
prompt = st.chat_input("KutiAI'ye bir komut veya mesaj gönder...")

if prompt:
    # 1. Senin mesajını ekrana yaz ve hafızaya al
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Asistanın cevabını al ve ekrana yaz
    with st.chat_message("assistant"):
        try:
            # Google sunucularına istek atılır
            response = model.generate_content(prompt)
            ai_cevap = response.text
            
            # Cevap ekrana yazılır ve hafızaya kaydedilir
            st.markdown(ai_cevap)
            st.session_state.messages.append({"role": "assistant", "content": ai_cevap})
        
        except Exception as e:
            # Eğer Google tarafında bir çökme olursa sistemi dondurmaz, sadece hata mesajı verir
            st.error(f"SİSTEM HATASI (API Kaynaklı): {e}")
