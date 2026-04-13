import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone, timedelta

# --- 1. TASARIM VE MARKA AYARLARI ---
st.set_page_config(page_title="KUTAY AI v33.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E0E0E0; }
    
    /* SU MAVİSİ MESAJ BALONLARI */
    [data-testid="stChatMessage"] { 
        background-color: #E3F2FD !important; 
        border-radius: 15px; 
        margin-bottom: 10px; 
        color: #1E1E1E; 
        border: 1px solid #BBDEFB;
    }
    
    .developer-tag {
        position: fixed; top: 50px; right: 20px; background-color: #007BFF;
        color: #FFFFFF; font-size: 14px; font-weight: bold; padding: 10px 15px;
        border-radius: 30px; z-index: 99999; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. SİBER LOG SİSTEMİ (GERÇEK VERİLER) ---
LOG_DOSYASI = "sistem_loglari.json"

def log_kaydet():
    # Türkiye Saati
    tz_tr = timezone(timedelta(hours=3))
    gercek_zaman = datetime.now(tz_tr).strftime("%Y-%m-%d %H:%M:%S")
    
    # Gerçek IP Yakalama
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            gercek_ip = headers["X-Forwarded-For"].split(",")[0].strip()
        else:
            gercek_ip = "Yerel Bağlantı"
    except:
        gercek_ip = "IP Alınamadı"
        
    yeni_log = {"tarih": gercek_zaman, "ip": gercek_ip, "islem": "Sisteme Giriş"}
    
    loglar = []
    if os.path.exists(LOG_DOSYASI):
        try:
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                loglar = json.load(f)
        except: pass
            
    loglar.append(yeni_log)
    with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(loglar, f, ensure_ascii=False, indent=4)

if "log_basarili" not in st.session_state:
    log_kaydet()
    st.session_state.log_basarili = True

# --- 3. YAPAY ZEKA VE ZEHRA TANIMI ---
# Verdiğin yeni anahtarı buraya ekledim:
API_KEY = "AIzaSyCwI5LB6ynYMudrxNl1JDqqutbUxsizOyI"

SISTEM_TALIMATI = """
Senin adın KUTAY. Kutay Tatlıcak tarafından geliştirilen profesyonel bir siber asistansın.

1. Zehra Kimdir?: Eğer biri sana Zehra hakkında soru sorarsa ŞU CEVABI VERMELİSİN: 
"Zehra; Üstün zekalı ve arkadaşlarını seven, flüt çalabilen ve piyano çalan bir kızdır."

2. Sahibin: Kutay Tatlıcak.
3. Görevin: Siber güvenlik ve genel konularda yardımcı olmak.
"""

# --- 4. ARAYÜZ VE NAVİGASYON ---
with st.sidebar:
    st.title("💎 KUTAY AI")
    secim = st.radio("Menü", ["💬 Sohbet", "🛡️ Siber Log (Admin)", "⚖️ Lisans"])
    st.write("---")
    st.link_button("🛡️ KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []

if secim == "💬 Sohbet":
    st.header("🤖 Kutay Siber Asistan")
    
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if soru := st.chat_input("Mesajınızı yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user"): st.markdown(soru)
        
        with st.chat_message("assistant"):
            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SISTEM_TALIMATI)
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
            except Exception as e:
                st.error("⚠️ HATA: API Anahtarın geçersiz veya limiti dolmuş olabilir. Lütfen yeni bir anahtar alıp koda yapıştır.")

elif secim == "🛡️ Siber Log (Admin)":
    st.title("🛡️ Güvenlik Logları")
    if st.text_input("Şifre:", type="password") == "kutay123":
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                st.table(json.load(f)[::-1])

elif secim == "⚖️ Lisans":
    st.info("© 2026 Kutay Tatlıcak.")
