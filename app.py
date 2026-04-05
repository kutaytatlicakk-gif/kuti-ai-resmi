import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. MARKA VE SAYFA AYARLARI ---
st.set_page_config(page_title="KUTAY AI", page_icon="💎", layout="wide")

# CSS ile Google Gemini stili menü ve tasarım
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3136,#2e3136); }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #3e4147; }
    footer {visibility: hidden;}
    .reportview-container .main footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİK VE API (KASA SİSTEMİ) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ SİSTEM DURDURULDU: API Anahtarı Secrets kısmında bulunamadı!")
    st.stop()

# --- 3. DİNAMİK MODEL MOTORU (404 HATASINI BİTİREN KISIM) ---
@st.cache_resource
def model_bagla():
    try:
        # Google'ın o an sunduğu çalışan modelleri otomatik tara
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # En hızlı ve güncel olanı seç (Flash 1.5 öncelikli)
        for m in modeller:
            if "1.5-flash" in m: return genai.GenerativeModel(m)
        return genai.GenerativeModel(modeller[0])
    except Exception as e:
        st.error(f"Model Motoru Başlatılamadı: {e}")
        st.stop()

model = model_bagla()

# --- 4. VERİ YÖNETİMİ ---
CHAT_DIR = "arsiv"
if not os.path.exists(CHAT_DIR): os.makedirs(CHAT_DIR)

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []
if "session_id" not in st.session_state: st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M")

# --- 5. PROFESYONEL YAN MENÜ (FOTOĞRAFTAKİ GİBİ) ---
with st.sidebar:
    st.title("💎 KUTAY")
    
    # Menü Seçenekleri
    menu = st.radio("", ["💬 Sohbet", "⚙️ Ayarlar", "⚖️ Kullanım Hakları"])
    
    st.write("---")
    
    if st.button("➕ Yeni Sohbet"):
        st.session_state.mesajlar = []
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M")
        st.rerun()

    st.subheader("🕒 Sohbetler")
    # Kayıtlı dosyaları listele
    files = sorted([f for f in os.listdir(CHAT_DIR) if f.endswith(".json")], reverse=True)
    for f in files:
        cid = f.replace(".json", "")
        if st.button(f"📄 {cid}", key=cid):
            with open(f"{CHAT_DIR}/{f}", "r", encoding="utf-8") as fin:
                st.session_state.mesajlar = json.load(fin)
                st.session_state.session_id = cid
            st.rerun()

# --- 6. SAYFA İÇERİKLERİ ---

if menu == "💬 Sohbet":
    st.title("🤖 Kutay Siber Asistan")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Özel Yapay Zeka")

    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Kutay'a bir mesaj gönder..."):
        st.session_state.mesajlar.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            try:
                r = model.generate_content(p)
                st.markdown(r.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": r.text})
                # Otomatik Yedekle
                with open(f"{CHAT_DIR}/{st.session_state.session_id}.json", "w", encoding="utf-8") as fout:
                    json.dump(st.session_state.mesajlar, fout, ensure_ascii=False)
            except Exception as e:
                st.error(f"Bağlantı Kesildi: {e}")

elif menu == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.write("---")
    st.write(f"**Aktif Model:** {model.model_name}")
    st.write("**Geliştirici:** Yusuf Tatlıcak")
    st.write("**Sürüm:** v20.0 Gold Edition")
    st.color_picker("Arayüz Rengi Seç (Yakında)", "#00f9ff")
    if st.button("Tüm Geçmişi Temizle"):
        for f in os.listdir(CHAT_DIR): os.remove(os.path.join(CHAT_DIR, f))
        st.success("Tüm veriler silindi.")

elif menu == "⚖️ Kullanım Hakları":
    st.title("⚖️ Telif ve Lisans Hakları")
    st.write("---")
    st.warning("Bu yazılımın tüm hakları **Yusuf Tatlıcak**'a aittir.")
    st.markdown("""
    ### 🛡️ Yasal Uyarı:
    * Bu kodun izinsiz kopyalanması, paylaşılması veya başka isimle yayınlanması yasaktır.
    * **KUTAY AI** ismi ve logosu marka koruması altındadır.
    * Açık kaynak olarak paylaşılsa dahi 'Geliştirici: Yusuf Tatlıcak' ibaresi kaldırılamaz.
    
    **© 2026 Kutay Software - Tüm Hakları Saklıdır.**
    """)
