import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI v28.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E0E0E0; }
    [data-testid="stChatMessage"] { 
        background-color: #E3F2FD !important; 
        border-radius: 15px; margin-bottom: 10px; color: #1E1E1E; border: 1px solid #BBDEFB;
    }
    .developer-tag {
        position: fixed; top: 50px; right: 20px; background-color: #007BFF;
        color: #FFFFFF; font-size: 14px; font-weight: bold; padding: 10px 15px;
        border-radius: 30px; z-index: 99999; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. LOG SİSTEMİ (GÜVENLİK) ---
LOG_DOSYASI = "sistem_loglari.json"

def log_kaydet():
    # Kullanıcı bilgilerini simüle ederek alıyoruz (Streamlit Cloud üzerinde headerlardan çekilir)
    try:
        user_ip = st.context.headers.get("X-Forwarded-For", "Bilinmiyor")
    except:
        user_ip = "Yerel Bağlantı"
        
    yeni_log = {
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": user_ip,
        "islem": "Sisteme Giriş Yapıldı"
    }
    
    loglar = []
    if os.path.exists(LOG_DOSYASI):
        with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
            loglar = json.load(f)
            
    loglar.append(yeni_log)
    with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(loglar, f, ensure_ascii=False, indent=4)

# Her girişte log tut
if "log_alindi" not in st.session_state:
    log_kaydet()
    st.session_state.log_alindi = True

# --- 3. YAPAY ZEKA MOTORU ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ API Anahtarı Bulunamadı!")
    st.stop()

SISTEM_TALIMATI = "Senin adın KUTAY. Kutay Tatlıcak tarafından geliştirilen profesyonel siber asistansın."

@st.cache_resource
def model_getir():
    modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    secilen_model = next((m for m in modeller if "1.5-flash" in m), modeller[0])
    return genai.GenerativeModel(model_name=secilen_model, system_instruction=SISTEM_TALIMATI)

model = model_getir()

# --- 4. HAFIZA VE NAVİGASYON ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)
if "mesajlar" not in st.session_state: st.session_state.mesajlar = []

with st.sidebar:
    st.title("💎 KUTAY AI")
    secim = st.radio("", ["💬 Sohbet", "⚙️ Ayarlar", "⚖️ Haklar", "🛡️ Siber Log (Admin)"])
    st.write("---")
    st.link_button("🛡️ KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")

# --- 5. SAYFALAR ---

if secim == "💬 Sohbet":
    st.header("🤖 Kutay Siber Asistan")
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if soru := st.chat_input("Mesajınız..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user"): st.markdown(soru)
        with st.chat_message("assistant"):
            cevap = model.generate_content(soru)
            st.markdown(cevap.text)
            st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})

elif secim == "🛡️ Siber Log (Admin)":
    st.title("🛡️ Güvenlik ve IP Logları")
    # Sadece senin bileceğin bir şifre (Burayı değiştirebilirsin)
    sifre = st.text_input("Geliştirici Şifresini Girin:", type="password")
    
    if sifre == "kutay123": # <--- Şifren bu!
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                veriler = json.load(f)
            st.success(f"Toplam {len(veriler)} giriş kaydı bulundu.")
            st.table(veriler[::-1]) # En son girişi en üstte göster
        else:
            st.info("Henüz kayıtlı log yok.")
    elif sifre != "":
        st.error("Yetkisiz Giriş! IP Adresiniz loglara kaydedildi.")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Lisans ve Haklar")
    st.info("© 2026 Kutay Tatlıcak. Tüm Hakları Saklıdır.")
    st.write("Bu yazılımın izinsiz kopyalanması ve kullanılması durumunda log kayıtları yasal mercilere iletilecektir.")
