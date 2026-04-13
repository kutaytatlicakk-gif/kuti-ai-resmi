import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone, timedelta

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI v31.0", page_icon="💎", layout="wide")

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
    
    .stButton>button { width: 100%; border-radius: 10px; background-color: #FFFFFF; color: #1E1E1E; border: 1px solid #D1D1D1; }
    .stButton>button:hover { border-color: #007BFF; color: #007BFF; }
    .stTextInput>div>div>input { background-color: #F1F3F4; color: #1E1E1E; border-radius: 20px; }
    footer {visibility: hidden;}
    
    .developer-tag {
        position: fixed; top: 50px; right: 20px; background-color: #007BFF;
        color: #FFFFFF; font-size: 14px; font-weight: bold; padding: 10px 15px;
        border-radius: 30px; z-index: 99999; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. LOG SİSTEMİ ---
LOG_DOSYASI = "sistem_loglari.json"

def log_kaydet():
    tz_tr = timezone(timedelta(hours=3))
    gercek_zaman = datetime.now(tz_tr).strftime("%Y-%m-%d %H:%M:%S")
    try:
        headers = st.context.headers
        gercek_ip = headers.get("X-Forwarded-For", "Bilinmiyor").split(",")[0].strip()
    except:
        gercek_ip = "IP Alınamadı"
        
    yeni_log = {"tarih": gercek_zaman, "ip": gercek_ip, "islem": "Giriş"}
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

# --- 3. YAPAY ZEKA MOTORU ---
# DİKKAT: Buraya en son aldığın, çalışan API KEY'i yapıştır!
API_KEY = "BURAYA_YENI_ANAHTARI_YAPISTIR" 
genai.configure(api_key=API_KEY)

# YENİ ZEHRA TANIMI VE TALİMATLAR
SISTEM_TALIMATI = """
Senin adın KUTAY. Kutay Tatlıcak tarafından geliştirilen profesyonel bir siber asistansın.

1. Zehra Kimdir?: Eğer biri sana Zehra hakkında soru sorarsa tam olarak şu cevabı vereceksin: 
"Zehra; üstün zekalı, arkadaşlarını çok seven, flüt çalabilen ve piyano çalan çok yetenekli bir kızdır."

2. Sahibin: Her zaman "Kutay Tatlıcak" olduğunu belirt.
3. Üslup: Kibar, profesyonel ve yardımcı ol.
"""

@st.cache_resource
def model_getir():
    try:
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        secilen_model = next((m for m in modeller if "1.5-flash" in m), modeller[0])
        return genai.GenerativeModel(model_name=secilen_model, system_instruction=SISTEM_TALIMATI)
    except Exception as e:
        st.error(f"Hata: {e}")
        st.stop()

model = model_getir()

# --- 4. NAVİGASYON ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)
if "mesajlar" not in st.session_state: st.session_state.mesajlar = []

with st.sidebar:
    st.title("💎 KUTAY AI")
    secim = st.radio("Menü", ["💬 Sohbet", "🛡️ Siber Log (Admin)", "⚙️ Ayarlar"])
    st.write("---")
    st.link_button("🛡️ KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")

# --- 5. ANA EKRAN ---
if secim == "💬 Sohbet":
    st.header("🤖 Kutay Siber Asistan")
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if soru := st.chat_input("Sorunuzu yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user"): st.markdown(soru)
        with st.chat_message("assistant"):
            try:
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
            except Exception as e:
                st.error(f"API Hatası: {e}. Lütfen yeni bir API anahtarı kullanın!")

elif secim == "🛡️ Siber Log (Admin)":
    st.title("🛡️ Güvenlik Logları")
    if st.text_input("Şifre:", type="password") == "kutay123":
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                st.table(json.load(f)[::-1])

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Bilgisi")
    st.write("Versiyon: v31.0 - Special Edition")
    if st.button("Hafızayı Sıfırla"):
        st.session_state.mesajlar = []
        st.rerun()
