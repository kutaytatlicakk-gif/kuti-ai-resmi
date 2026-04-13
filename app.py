import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone, timedelta

# --- 1. TASARIM VE GÖRÜNÜM ---
st.set_page_config(page_title="KUTAY AI v31.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stChatMessage"] { 
        background-color: #E3F2FD !important; 
        border-radius: 15px; border: 1px solid #BBDEFB;
    }
    .developer-tag {
        position: fixed; top: 50px; right: 20px; background-color: #007BFF;
        color: white; font-weight: bold; padding: 10px 15px; border-radius: 30px; z-index: 9999;
    }
    </style>
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİ LOG SİSTEMİ ---
LOG_DOSYASI = "sistem_loglari.json"

def log_yaz():
    tr_saati = datetime.now(timezone(timedelta(hours=3))).strftime("%Y-%m-%d %H:%M:%S")
    try:
        ip = st.context.headers.get("X-Forwarded-For", "Bilinmiyor").split(",")[0].strip()
    except: ip = "Alınamadı"
    
    yeni_kayit = {"tarih": tr_saati, "ip": ip, "islem": "Sisteme Giriş"}
    loglar = []
    if os.path.exists(LOG_DOSYASI):
        with open(LOG_DOSYASI, "r", encoding="utf-8") as f: loglar = json.load(f)
    loglar.append(yeni_kayit)
    with open(LOG_DOSYASI, "w", encoding="utf-8") as f: json.dump(loglar, f, indent=4)

if "log_tamam" not in st.session_state:
    log_yaz()
    st.session_state.log_tamam = True

# --- 3. YAPAY ZEKA AYARLARI ---
# BURAYA YENİ ALDIĞIN ANAHTARI KOYMALISIN:
YENI_API_KEY = "BURAYA_GOOGLE_AI_STUDIODAN_ALDIGIN_YENI_ANAHTARI_YAPISTIR"
genai.configure(api_key=YENI_API_KEY)

SISTEM_TALIMATI = """
Senin adın KUTAY. Kutay Tatlıcak tarafından geliştirildin.
ZEHRA HAKKINDA: Eğer biri sana Zehra'yı sorarsa şu cevabı ver: 
"Zehra; üstün zekalı ve arkadaşlarını seven, flüt çalabilen ve piyano çalan bir kızdır."
Sahibin: Kutay Tatlıcak.
"""

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SISTEM_TALIMATI)

# --- 4. ARAYÜZ ---
with st.sidebar:
    st.title("💎 KUTAY AI")
    secim = st.radio("Menü", ["💬 Sohbet", "🛡️ Admin Log", "⚖️ Lisans"])
    st.write("---")
    st.info("Sivas / Türkiye")

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []

if secim == "💬 Sohbet":
    st.header("🤖 Kutay Siber Asistan")
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]): st.write(m["content"])

    if soru := st.chat_input("Mesajınızı yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user"): st.write(soru)
        
        try:
            cevap = model.generate_content(soru).text
            with st.chat_message("assistant"): st.write(cevap)
            st.session_state.mesajlar.append({"role": "assistant", "content": cevap})
        except Exception as e:
            st.error("API Anahtarı Geçersiz! Lütfen yeni bir anahtar alıp koda yapıştır.")

elif secim == "🛡️ Admin Log":
    if st.text_input("Şifre:", type="password") == "kutay123":
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                st.table(json.load(f)[::-1])

elif secim == "⚖️ Lisans":
    st.write("© 2026 Kutay Tatlıcak. Tüm hakları saklıdır.")
