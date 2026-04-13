import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone, timedelta

# --- 1. TASARIM VE ARAYÜZ AYARLARI ---
st.set_page_config(page_title="KUTAY AI v32.0", page_icon="💎", layout="wide")

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

# --- 2. GELİŞMİŞ LOG SİSTEMİ ---
LOG_DOSYASI = "sistem_loglari.json"

def log_kaydet():
    # Türkiye Saati (UTC+3)
    tz_tr = timezone(timedelta(hours=3))
    gercek_zaman = datetime.now(tz_tr).strftime("%Y-%m-%d %H:%M:%S")
    
    # Gerçek Dış IP Yakalama
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            gercek_ip = headers["X-Forwarded-For"].split(",")[0].strip()
        else:
            gercek_ip = "Yerel/Bilinmiyor"
    except:
        gercek_ip = "IP Bulunamadı"
        
    yeni_log = {"tarih": gercek_zaman, "ip": gercek_ip, "islem": "Sisteme Giriş Yapıldı"}
    
    loglar = []
    if os.path.exists(LOG_DOSYASI):
        try:
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                loglar = json.load(f)
        except: pass
            
    loglar.append(yeni_log)
    with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(loglar, f, ensure_ascii=False, indent=4)

if "log_aktif" not in st.session_state:
    log_kaydet()
    st.session_state.log_aktif = True

# --- 3. YAPAY ZEKA VE TALİMATLAR ---
# BURAYA YENİ ANAHTARI YAPISTIR (DİKKAT: Paylaştığın fotoğraftaki hata budur)
YENI_API_KEY = "AIzaSyDLw1hBKxC9qO9Hw6OGbot90invzIuePpQ" 

SISTEM_TALIMATI = """
Senin adın KUTAY. Kutay Tatlıcak tarafından geliştirilen profesyonel bir siber asistansın.

1. Zehra Kimdir?: Eğer biri sana Zehra hakkında soru sorursa ŞU CEVABI VERMELİSİN: 
"Zehra; Üstün zekalı ve arkadaşlarını seven, flüt çalabilen ve piyano çalan bir kızdır."

2. Sahibin Kim?: Seni kimin yaptığını sorarlarsa her zaman "Kutay Tatlıcak" diyeceksin.
3. Davranış: Zeki, profesyonel ve yardımcı ol.
"""

@st.cache_resource
def model_baslat():
    try:
        genai.configure(api_key=YENI_API_KEY)
        return genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SISTEM_TALIMATI)
    except Exception as e:
        return None

model = model_baslat()

# --- 4. NAVİGASYON VE HAFIZA ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)
if "mesajlar" not in st.session_state: st.session_state.mesajlar = []

with st.sidebar:
    st.title("💎 KUTAY AI")
    st.subheader(f"Geliştirici: Kutay")
    secim = st.radio("Menü", ["💬 Sohbet", "🛡️ Siber Log (Admin)", "⚙️ Ayarlar", "⚖️ Lisans"])
    st.write("---")
    st.link_button("🛡️ KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")

# --- 5. ANA SAYFALAR ---

if secim == "💬 Sohbet":
    st.markdown("<h2 style='text-align: center;'>🤖 Kutay Siber Asistan</h2>", unsafe_allow_html=True)
    
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if soru := st.chat_input("Sorunuzu buraya yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user"): st.markdown(soru)
        
        if model:
            with st.chat_message("assistant"):
                try:
                    cevap = model.generate_content(soru)
                    st.markdown(cevap.text)
                    st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
                except Exception as e:
                    st.error("Hata: API Anahtarınız geçersiz veya süresi dolmuş. Lütfen yeni bir anahtar alın.")
        else:
            st.error("Sistem başlatılamadı. Lütfen geçerli bir API anahtarı girin.")

elif secim == "🛡️ Siber Log (Admin)":
    st.title("🛡️ Güvenlik ve IP Logları")
    sifre = st.text_input("Geliştirici Şifresi:", type="password")
    if sifre == "kutay123":
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                veriler = json.load(f)
            st.success(f"Sistem Kayıtları Aktif. Toplam {len(veriler)} giriş.")
            st.table(veriler[::-1])
        else:
            st.info("Henüz kayıt bulunamadı.")
    elif sifre != "":
        st.error("YETKİSİZ ERİŞİM! IP Adresiniz loglara kaydedilmiştir.")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Ayarlar")
    st.write("Sürüm: v32.0 Ultimate Siber Koruma")
    if st.button("Tüm Sohbet Hafızasını Sil"):
        st.session_state.mesajlar = []
        st.success("Hafıza başarıyla temizlendi!")

elif secim == "⚖️ Lisans":
    st.title("⚖️ Lisans ve Haklar")
    st.info("© 2026 Kutay Tatlıcak. Bu yazılımın tüm hakları saklıdır. İzinsiz paylaşılması durumunda loglardaki IP adresleri üzerinden yasal takip başlatılır.")
