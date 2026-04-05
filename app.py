import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI", page_icon="💎", layout="wide")

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
    </style>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİK VE MODEL MOTORU (KİŞİLİK AYARI EKLENDİ) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ SİSTEM DURDURULDU: API Anahtarı Bulunamadı!")
    st.stop()

@st.cache_resource
def model_getir():
    # ASİSTANA NASIL DAVRANMASI GEREKTİĞİNİ BURADA SÖYLÜYORUZ
    SISTEM_TALIMATI = """
    Sen Yusuf Tatlıcak tarafından geliştirilen 'KUTAY' isimli siber asistansın. 
    Görevin kullanıcıyla doğal, zeki ve samimi bir şekilde sohbet etmektir.
    ASLA kullanıcının yazdığı kelimeleri veya cümleleri dil bilgisi, sözlük anlamı veya 'ne anlama gelir' şeklinde analiz ederek açıklama. 
    Bir sözlük veya öğretmen gibi davranma. Sadece sorulan soruya veya söylenen söze bir arkadaş veya asistan gibi cevap ver.
    Cevapların kısa, öz ve amaca yönelik olsun.
    """
    try:
        # 1.5-flash modelini sistem talimatıyla başlat
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SISTEM_TALIMATI
        )
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
    st.markdown(f"<p style='text-align: center; color: #757575;'>Geliştirici: Yusuf Tatlıcak</p>", unsafe_allow_html=True)

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
                st.error(f"Bağlantı Hatası: {e}")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.write(f"**Yazılım Sahibi:** Yusuf Tatlıcak")
    st.write(f"**Güncel Sürüm:** v25.0 Diamond Shield + Social Intelligence")
    if st.button("🗑️ Tüm Hafızayı Sil"):
        for f in os.listdir(KAYIT_YOLU): os.remove(os.path.join(KAYIT_YOLU, f))
        st.success("Tüm geçmiş temizlendi!")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Kullanım ve Lisans Hakları")
    st.warning("Bu yazılımın tüm fikri ve sınai hakları Yusuf Tatlıcak'a aittir.")
    
    st.markdown("""
    ### 🛡️ KUTAY AI Gelişmiş Yazılım Sözleşmesi
    
    **1. Fikri Mülkiyet ve Marka Hakları:**
    Bu yazılımın tüm kaynak kodları, görsel arayüzü, kullanılan logolar ve "KUTAY" markası **Yusuf Tatlıcak** adına tescillidir. Bu kodların izinsiz olarak GitHub veya diğer platformlarda başka bir isimle paylaşılması yasaldır.
    
    **2. Siber Güvenlik ve Gizlilik:**
    KUTAY AI, kullanıcı güvenliğini ön planda tutar. Paylaşılan veriler sadece yerel oturumda ve kullanıcıya özel arşiv klasöründe saklanır. API anahtarları asla üçüncü şahıslarla paylaşılmaz.
    
    **3. Kullanım Koşulları:**
    Yazılımın "öğretmen modu" veya "sözlük modu" gibi davranması, Yusuf Tatlıcak tarafından optimize edilen sistem talimatlarıyla engellenmiştir. Kullanıcı, yazılımı kişisel yardım ve sohbet amacıyla kullanmayı kabul eder.
    
    **4. Sorumluluk Sınırları:**
    Model tarafından üretilen yanıtlar yapay zeka ürünüdür. Yusuf Tatlıcak, yanıtların içeriğinden dolayı hukuki sorumluluk kabul etmez; ancak sistemin her zaman en doğru ve etik şekilde çalışması için güncellemeler yapar.
    
    **5. Geliştirici Beyanı:**
    Bu proje, 6. sınıf öğrencisi Yusuf Tatlıcak'ın yazılım ve yapay zeka konusundaki yeteneklerini sergileyen profesyonel bir çalışmadır. Tüm güncellemeler geliştirici tarafından denetlenir.
    
    ---
    **© 2026 Yusuf Tatlıcak Software. Tüm Hakları Saklıdır.**
    """)
