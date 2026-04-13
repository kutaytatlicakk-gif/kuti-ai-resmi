import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone, timedelta

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI v30.0", page_icon="💎", layout="wide")

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
    
    /* SAĞ ÜST KÖŞE GELİŞTİRİCİ ETİKETİ */
    .developer-tag {
        position: fixed; top: 50px; right: 20px; background-color: #007BFF;
        color: #FFFFFF; font-size: 14px; font-weight: bold; padding: 10px 15px;
        border-radius: 30px; z-index: 99999; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. LOG SİSTEMİ (GERÇEK VERİLER) ---
LOG_DOSYASI = "sistem_loglari.json"

def log_kaydet():
    # TÜRKİYE SAATİ (UTC+3)
    tz_tr = timezone(timedelta(hours=3))
    gercek_zaman = datetime.now(tz_tr).strftime("%Y-%m-%d %H:%M:%S")
    
    # GERÇEK DIŞ IP YAKALAMA
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            gercek_ip = headers["X-Forwarded-For"].split(",")[0].strip()
        else:
            gercek_ip = "Yerel Bağlantı / Bilinmiyor"
    except:
        gercek_ip = "Hata: IP Alınamadı"
        
    yeni_log = {
        "tarih": gercek_zaman,
        "ip": gercek_ip,
        "islem": "Sisteme Giriş"
    }
    
    loglar = []
    if os.path.exists(LOG_DOSYASI):
        try:
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                loglar = json.load(f)
        except: pass
            
    loglar.append(yeni_log)
    with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(loglar, f, ensure_ascii=False, indent=4)

# Her oturumda bir kez log al
if "log_basarili" not in st.session_state:
    log_kaydet()
    st.session_state.log_basarili = True

# --- 3. GÜVENLİK VE YAPAY ZEKA MOTORU ---
# Yeni aldığın ve çalışan anahtar
API_KEY = "AIzaSyC5_Wo4KqbTwcserdyxUQRhIfhmWgq6EFo"
genai.configure(api_key=API_KEY)

# ÖZEL TALİMATLAR (ZEHRA ŞAKASI DAHİL)
SISTEM_TALIMATI = """
Senin adın KUTAY. Sen Kutay Tatlıcak tarafından geliştirilen profesyonel bir siber asistansın.

1. Zehra Kimdir?: Eğer biri sana "Zehra kim?", "Zehra'yı tanıyor musun?" gibi sorular sorarsa şu cevabı vereceksin: 
"Zehra; Brawl Stars bağımlısı, obezler gibi oynayan, hayatında bir kere bile çimen görmemiş, Kutay'ın arkadaşıdır."

2. Sahibin Kim?: Seni kimin yaptığını sorarlarsa cevabın "Kutay Tatlıcak" olmalıdır.
3. Davranış: Profesyonel, zeki ve doğal konuş. 
4. Kural: Kelime anlamlarını sözlük gibi açıklama. Sadece sohbete odaklan.
"""

@st.cache_resource
def model_getir():
    try:
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        secilen_model = next((m for m in modeller if "1.5-flash" in m), modeller[0])
        return genai.GenerativeModel(model_name=secilen_model, system_instruction=SISTEM_TALIMATI)
    except Exception as e:
        st.error(f"Sistem Başlatılamadı: {e}")
        st.stop()

model = model_getir()

# --- 4. VERİ VE HAFIZA ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []
if "aktif_id" not in st.session_state: st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 5. SOL PANEL ---
with st.sidebar:
    st.title("💎 KUTAY AI")
    st.write(f"Hoş geldin, **Kutay**")
    secim = st.radio("Menü", ["💬 Sohbet", "🛡️ Siber Log (Admin)", "⚙️ Ayarlar", "⚖️ Haklar"])
    
    st.write("---")
    st.markdown("### 🛡️ Güvenlik")
    st.link_button("KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    st.write("---")
    
    if st.button("➕ Yeni Sohbet"):
        st.session_state.mesajlar = []
        st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

# --- 6. SAYFALAR ---

if secim == "💬 Sohbet":
    st.markdown("<h2 style='text-align: center;'>🤖 Kutay Siber Asistan</h2>", unsafe_allow_html=True)
    
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if soru := st.chat_input("Buraya yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user"):
            st.markdown(soru)
        
        with st.chat_message("assistant"):
            try:
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
                # Otomatik Kaydet
                with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.mesajlar, f, ensure_ascii=False)
            except Exception as e:
                st.error(f"Hata: {e}")

elif secim == "🛡️ Siber Log (Admin)":
    st.title("🛡️ Güvenlik ve IP Kayıtları")
    sifre = st.text_input("Geliştirici Şifresi:", type="password")
    
    if sifre == "kT2.0.1.4":
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                veriler = json.load(f)
            st.success(f"Sistem Aktif. Toplam {len(veriler)} giriş kaydedildi.")
            st.table(veriler[::-1]) # En yeni en üstte
        else:
            st.info("Henüz log kaydı oluşmadı.")
    elif sifre != "":
        st.error("YETKİSİZ ERİŞİM DENEMESİ!")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Ayarlar")
    st.info("Geliştirici: Kutay Tatlıcak | Sürüm: v30.0 Ultimate")
    if st.button("🗑️ Tüm Sohbetleri Temizle"):
        for f in os.listdir(KAYIT_YOLU): os.remove(os.path.join(KAYIT_YOLU, f))
        st.success("Tüm geçmiş silindi!")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Lisans")
    st.markdown("""
    ### 🛡️ KUTAY AI Resmi Lisansı
    * Bu yazılımın tüm mülkiyet hakları **Kutay Tatlıcak**'a aittir.
    * İzinsiz paylaşılması veya kodların çalınması durumunda yasal işlem başlatılır.
    * **© 2026 Kutay Tatlıcak. Tüm Hakları Saklıdır.**
    """)
