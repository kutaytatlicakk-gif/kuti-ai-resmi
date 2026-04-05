import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI", page_icon="💎", layout="wide")

# CSS: Su mavisi mesaj balonları ve SAĞ ALT KÖŞE GELİŞTİRİCİ YAZISI
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
    
    /* SAĞ ALT KÖŞE GELİŞTİRİCİ ETİKETİ (WATERMARK) */
    .developer-watermark {
        position: fixed;
        bottom: 15px;
        right: 15px;
        background-color: #F8F9FA;
        color: #333333;
        font-size: 13px;
        font-weight: bold;
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid #D1D1D1;
        z-index: 99999;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        backdrop-filter: blur(5px);
    }
    </style>
    
    <div class="developer-watermark">
        🛡️ Geliştirici: Kutay Tatlıcak
    </div>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİK VE YAPAY ZEKA MOTORU ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ SİSTEM DURDURULDU: API Anahtarı Bulunamadı!")
    st.stop()

# YAPAY ZEKANIN KİŞİLİK VE KİMLİK AYARLARI
SISTEM_TALIMATI = """
Senin adın KUTAY. Sen Kutay Tatlıcak tarafından özel olarak geliştirilen, üst düzey bir siber asistansın.
1. Senin sahibin, yaratıcın ve tek geliştiricin Kutay Tatlıcak'tır. Biri sana sahibini, kimin yaptığını veya geliştiricini sorarsa kesinlikle 'Kutay Tatlıcak' (veya Kutay) olarak cevap vermelisin.
2. Kullanıcıyla doğal, zeki, amaca yönelik ve profesyonel bir şekilde sohbet et.
3. ASLA kullanıcının yazdığı kelimeleri sözlük gibi açıklama. "Ne anlama gelir", "kelime anlamı şudur" gibi tanımlamalar yapma. Türkçe öğretmeni değilsin, sen bir siber asistansın. Sadece sorulana net ve doğal cevaplar ver. "Hepsi" gibi kelimeleri tanımlama.
"""

@st.cache_resource
def model_getir():
    try:
        # 404 Hatasını çözen dinamik model bulucu
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Öncelikli olarak flash bulmaya çalış, bulamazsa hesabındaki ilk çalışan modeli al
        secilen_model = modeller[0] 
        for m in modeller:
            if "1.5-flash" in m:
                secilen_model = m
                break

        try:
            return genai.GenerativeModel(model_name=secilen_model, system_instruction=SISTEM_TALIMATI)
        except:
            # Eski SDK sürümleri için güvenlik önlemi
            return genai.GenerativeModel(model_name=secilen_model)
            
    except Exception as e:
        st.error(f"Sistem Başlatılamadı: {e}")
        st.stop()

model = model_getir()

# --- 3. VERİ SİSTEMİ VE HAFIZA ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []
if "aktif_id" not in st.session_state: st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 4. HATA ÖNLEYİCİ PP KONTROLÜ ---
def user_pp_getir():
    if os.path.exists("user_pp.png"): return "user_pp.png"
    return "👤"

def ai_pp_getir():
    if os.path.exists("ai_diamond.png"): return "ai_diamond.png"
    return "💎"

# --- 5. SOL PANEL ---
with st.sidebar:
    ai_p = ai_pp_getir()
    if os.path.exists(ai_p) and ai_p != "💎":
        st.image(ai_p, width=50)
    else:
        st.markdown(f"<h2>{ai_p}</h2>", unsafe_allow_html=True)
            
    st.title("KUTAY")
    secim = st.radio("", ["💬 Sohbet", "⚙️ Ayarlar", "⚖️ Haklar"])
    st.write("---")
    
    if st.button("➕ Yeni Sohbet"):
        st.session_state.mesajlar = []
        st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.subheader("🕒 Geçmiş Sohbetler")
    dosyalar = sorted([f for f in os.listdir(KAYIT_YOLU) if f.endswith(".json")], reverse=True)
    for dosya in dosyalar:
        dosya_yolu = os.path.join(KAYIT_YOLU, dosya)
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                veriler = json.load(f)
                baslik = veriler[0]["content"][:25] + "..." if veriler else dosya
        except:
            baslik = "Boş Sohbet"
            
        if st.button(f"💬 {baslik}", key=dosya):
            with open(dosya_yolu, "r", encoding="utf-8") as f_yukle:
                st.session_state.mesajlar = json.load(f_yukle)
                st.session_state.aktif_id = dosya.replace(".json", "")
            st.rerun()

# --- 6. SAYFA İÇERİKLERİ ---

if secim == "💬 Sohbet":
    st.markdown(f"<h2 style='text-align: center; color: #1E1E1E;'>🤖 Kutay Siber Asistan</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #757575;'>Geliştirici: Kutay Tatlıcak</p>", unsafe_allow_html=True)

    user_p = user_pp_getir()
    ai_p = ai_pp_getir()

    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"], avatar=user_p if m["role"] == "user" else ai_p):
            st.markdown(m["content"])

    if soru := st.chat_input("Mesajınızı buraya yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user", avatar=user_p):
            st.markdown(soru)
        
        with st.chat_message("assistant", avatar=ai_p):
            try:
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
                
                with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f_kayit:
                    json.dump(st.session_state.mesajlar, f_kayit, ensure_ascii=False)
            except Exception as e:
                st.error(f"Sistem Yanıt Hatası: {e}")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.write(f"**Yazılım Sahibi:** Kutay Tatlıcak")
    st.write(f"**Güncel Sürüm:** v26.0 Master Edition")
    if st.button("🗑️ Tüm Hafızayı Sil"):
        for f in os.listdir(KAYIT_YOLU): os.remove(os.path.join(KAYIT_YOLU, f))
        st.success("Tüm geçmiş temizlendi!")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Kullanım ve Lisans Hakları")
    st.warning("Bu yazılımın tüm fikri ve sınai hakları Kutay Tatlıcak'a aittir.")
    
    st.markdown("""
    ### 🛡️ KUTAY AI Profesyonel Yazılım Sözleşmesi
    
    **1. Fikri Mülkiyet ve Marka Hakları:**
    Bu yazılımın tüm kaynak kodları, görsel arayüzü, sistem mimarisi, logoları ve "KUTAY" markası tamamen **Kutay Tatlıcak** adına tescillidir. Kodların izinsiz olarak çoğaltılması, kopyalanması veya başka projelerde isim değiştirilerek kullanılması kesinlikle yasaktır.
    
    **2. Siber Güvenlik ve Gizlilik:**
    KUTAY AI, veri güvenliğini en üst düzeyde tutar. Kullanıcı sohbet geçmişi ve verileri yalnızca yerel klasörlerde barındırılır. Sisteme entegre edilen API anahtarları şifrelenmiş Secrets altyapısı ile korunur ve hiçbir koşulda üçüncü taraflarla paylaşılmaz.
    
    **3. Kullanım Koşulları:**
    Bu sistem, özel bir siber asistan olarak yapılandırılmıştır. Sözlük, çevirmen veya dil bilgisi öğretmeni gibi standart bot davranışları göstermez. Kullanıcı, yapay zekanın asistanlık sınırları çerçevesinde işlem yapmayı kabul eder.
    
    **4. Sorumluluk Sınırları:**
    Yazılımın temel veri işleme motoru dış kaynaklı API'lerle desteklenmektedir. Sistemin ürettiği sonuçlardan doğabilecek teknik aksaklıklar veya yanlış bilgilerden doğrudan sistem sahibi sorumlu tutulamaz. Geliştirici, sistemi her zaman stabil tutmak için güncellemeler sağlar.
    
    **5. Geliştirici Beyanı:**
    Bu proje, **Kutay Tatlıcak** tarafından sıfırdan dizayn edilmiş, profesyonel standartlarda kodlanmış bir yapay zeka entegrasyonudur. Her türlü güncelleme, değişiklik ve kapatma hakkı sadece geliştiriciye aittir.
    
    ---
    **© 2026 Kutay Tatlıcak Software. Tüm Hakları Saklıdır.**
    """)
