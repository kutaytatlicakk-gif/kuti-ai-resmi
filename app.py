import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. SAYFA VE BEYAZ TEMA AYARLARI ---
st.set_page_config(page_title="KUTAY AI", page_icon="💎", layout="wide")

# CSS: Beyaz tema, koyu yazılar, modern butonlar
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E0E0E0; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #FFFFFF; color: #1E1E1E; border: 1px solid #D1D1D1; }
    .stButton>button:hover { border-color: #007BFF; color: #007BFF; }
    .stTextInput>div>div>input { background-color: #F1F3F4; color: #1E1E1E; border-radius: 20px; }
    footer {visibility: hidden;}
    /* Sohbet balonlarını netleştirir */
    [data-testid="stChatMessage"] { background-color: #F1F3F4; border-radius: 15px; margin-bottom: 10px; color: #1E1E1E; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİK VE MODEL MOTORU ---
# API Anahtarını Secrets kısmından çek
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ SİSTEM DURDURULDU: API Anahtarı Secrets kısmında bulunamadı!")
    st.stop()

# Akıllı Model Motoru: Flash ve Pro otomatik seçer (404 hatasını bitirir)
@st.cache_resource
def model_getir():
    try:
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in modeller:
            if "1.5-flash" in m: return genai.GenerativeModel(m)
        return genai.GenerativeModel(modeller[0])
    except Exception as e:
        st.error(f"Sistem Başlatılamadı: {e}")
        st.stop()

model = model_getir()

# --- 3. VERİ SİSTEMİ VE HAFIZA ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []
if "aktif_id" not in st.session_state: st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 4. HATA ÖNLEYİCİ PP KONTROLÜ (KESİN ÇÖZÜM) ---
# Resim dosyaları yüklü mü kontrol et, yoksa emoji kullan
def user_pp_getir():
    if os.path.exists("user_pp.png"):
        return "user_pp.png"
    return "👤" # Dosya yoksa insan emojisi

def ai_pp_getir():
    if os.path.exists("ai_diamond.png"):
        return "ai_diamond.png"
    return "💎" # Dosya yoksa elmas emojisi (image_14.png'ye uygun)

# --- 5. SOL PANEL (KONU BAŞLIKLI GEÇMİŞ) ---
with st.sidebar:
    # Sol paneldeki pp resmi için kırılma kontrolü yap
    with st.spinner("💎 KUTAY markası yükleniyor..."):
        ai_p = ai_pp_getir()
        if os.path.exists(ai_p) and ai_p != "💎":
            st.image(ai_p, width=50)
        else:
            st.markdown(f"<h2>{ai_p}</h2>", unsafe_allow_html=True)
            
    st.title("KUTAY")
    
    secim = st.radio("", ["💬 Sohbet", "⚙️ Ayarlar", "⚖️ Haklar"])
    st.write("---")
    
    if st.button("➕ Yeni Sohbet"):
        if st.session_state.mesajlar:
            # Mevcut sohbeti kaydet
            with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f_kayit:
                json.dump(st.session_state.mesajlar, f_kayit, ensure_ascii=False)
        st.session_state.mesajlar = []
        st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.subheader("🕒 Geçmiş Sohbetler")
    
    # Arşivdeki dosyaları tara ve içindeki İLK MESAJI başlık yap
    dosyalar = sorted([f for f in os.listdir(KAYIT_YOLU) if f.endswith(".json")], reverse=True)
    for dosya in dosyalar:
        dosya_yolu = os.path.join(KAYIT_YOLU, dosya)
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                veriler = json.load(f)
                # Tarih yerine ilk mesajın ilk 25 karakterini başlık yap
                baslik = veriler[0]["content"][:25] + "..." if veriler else dosya
        except:
            baslik = "Boş Sohbet"
            
        if st.button(f"💬 {baslik}", key=dosya):
            # Geçerli sohbeti kaydetmeden yükleme
            if st.session_state.mesajlar:
                with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f_kayit:
                    json.dump(st.session_state.mesajlar, f_kayit, ensure_ascii=False)
            with open(dosya_yolu, "r", encoding="utf-8") as f_yukle:
                st.session_state.mesajlar = json.load(f_yukle)
                st.session_state.aktif_id = dosya.replace(".json", "")
            st.rerun()

# --- 6. SAYFA İÇERİKLERİ ---

if secim == "💬 Sohbet":
    st.markdown(f"<h2 style='text-align: center; color: #1E1E1E;'>🤖 Kutay Siber Asistan</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #757575;'>Yusuf Tatlıcak Tarafından Geliştirildi</p>", unsafe_allow_html=True)

    # Sohbet profillerini bir kez kontrol edelim
    user_p = user_pp_getir()
    ai_p = ai_pp_getir()

    # Mesajları Görüntüle
    for m in st.session_state.mesajlar:
        if m["role"] == "user":
            with st.chat_message("user", avatar=user_p):
                st.markdown(m["content"])
        else:
            with st.chat_message("assistant", avatar=ai_p):
                st.markdown(m["content"])

    # Kullanıcı Yazınca
    if soru := st.chat_input("Mesajınızı buraya yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user", avatar=user_p):
            st.markdown(soru)
        
        with st.chat_message("assistant", avatar=ai_p):
            try:
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
                
                # Saniyeler içinde kaydet (Her cevapta yedekleme)
                with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f_kayit:
                    json.dump(st.session_state.mesajlar, f_kayit, ensure_ascii=False)
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.write(f"**Yazılım Sahibi:** Yusuf Tatlıcak")
    st.write(f"**Sürüm:** v22.0 Gold Sürümü")
    st.write(f"**Bağlı Model:** {model.model_name}")
    st.write("**Model Motoru Durumu:** Aktif ve Stabil")
    st.markdown("---")
    st.subheader("💾 Veri Yönetimi")
    if st.button("🗑️ Tüm Sohbet Hafızasını Sil"):
        for f in os.listdir(KAYIT_YOLU): os.remove(os.path.join(KAYIT_YOLU, f))
        st.success("Tüm geçmiş temizlendi!")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Kullanım ve Telif Hakları")
    st.info("Bu proje tamamen Yusuf Tatlıcak'a aittir.")
    st.markdown("""
    1. **Mülkiyet:** Bu yazılımın kod yapısı ve tasarımı Yusuf Tatlıcak adına tescillidir.
    2. **Kopyalama:** Kodların izinsiz kopyalanması veya başka projelerde 'Kutay' ismi silinerek kullanılması yasaktır.
    3. **Güvenlik:** API anahtarı güvenliği Streamlit Secrets ile sağlanmaktadır.
    
    **© 2026 KUTAY Software. Tüm Hakları Saklıdır.**
    """)
