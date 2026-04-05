import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI", page_icon="💎", layout="wide")

# CSS: Su mavisi balonlar ve SAĞ ÜST KÖŞE GELİŞTİRİCİ ETİKETİ
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
    
    /* SAĞ ÜST KÖŞE GELİŞTİRİCİ ETİKETİ (WATERMARK) */
    .developer-tag {
        position: fixed;
        top: 50px;
        right: 20px;
        background-color: #007BFF;
        color: #FFFFFF;
        font-size: 14px;
        font-weight: bold;
        padding: 10px 15px;
        border-radius: 30px;
        z-index: 99999;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        border: 2px solid #FFFFFF;
    }
    </style>
    
    <div class="developer-tag">
        🛡️ Geliştirici: Kutay Tatlıcak
    </div>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİK VE YAPAY ZEKA MOTORU ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ SİSTEM DURDURULDU: API Anahtarı Bulunamadı!")
    st.stop()

SISTEM_TALIMATI = """
Senin adın KUTAY. Sen Kutay Tatlıcak tarafından geliştirilen profesyonel bir siber asistansın.
1. Sahibin Kim?: Biri sana "Sahibin kim?", "Seni kim yaptı?", "Geliştiricin kim?" gibi sorular sorarsa cevabın her zaman "Kutay Tatlıcak" (veya Kutay) olmalıdır. 
2. Davranış: Profesyonel, zeki ve doğal konuş. 
3. Kural: Kelime anlamlarını sözlük gibi açıklama. "Hepsi" veya benzeri kelimelerin tanımını yapma. Sadece sohbete odaklan.
"""

@st.cache_resource
def model_getir():
    try:
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        secilen_model = next((m for m in modeller if "1.5-flash" in m), modeller[0])
        return genai.GenerativeModel(model_name=secilen_model, system_instruction=SISTEM_TALIMATI)
    except Exception as e:
        st.error(f"Model Hatası: {e}")
        st.stop()

model = model_getir()

# --- 3. VERİ VE HAFIZA ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []
if "aktif_id" not in st.session_state: st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 4. PROFİL RESMİ KONTROLLERİ ---
def get_avatar(role):
    if role == "user":
        return "user_pp.png" if os.path.exists("user_pp.png") else "👤"
    return "ai_diamond.png" if os.path.exists("ai_diamond.png") else "💎"

# --- 5. SOL PANEL (NAVİGASYON) ---
with st.sidebar:
    st.markdown(f"<h1 style='text-align: center;'>{get_avatar('assistant')}</h1>", unsafe_allow_html=True)
    st.title("KUTAY AI")
    st.write(f"Hoş geldin, **Kutay**")
    secim = st.radio("", ["💬 Sohbet", "⚙️ Ayarlar", "⚖️ Haklar"])
    
    st.write("---")
    # EKLEDİĞİM LİNK BURADA:
    st.markdown("### 🛡️ Güvenlik Sistemi")
    st.link_button("KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.write("---")
    
    if st.button("➕ Yeni Sohbet"):
        st.session_state.mesajlar = []
        st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.subheader("🕒 Sohbet Geçmişi")
    dosyalar = sorted([f for f in os.listdir(KAYIT_YOLU) if f.endswith(".json")], reverse=True)
    for dosya in dosyalar[:10]:
        with open(os.path.join(KAYIT_YOLU, dosya), "r", encoding="utf-8") as f:
            v = json.load(f)
            baslik = v[0]["content"][:20] + "..." if v else dosya
        if st.button(f"💬 {baslik}", key=dosya):
            st.session_state.mesajlar = v
            st.session_state.aktif_id = dosya.replace(".json", "")
            st.rerun()

# --- 6. SAYFA İÇERİKLERİ ---

if secim == "💬 Sohbet":
    st.markdown("<h2 style='text-align: center;'>🤖 Kutay Siber Asistan</h2>", unsafe_allow_html=True)
    
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"], avatar=get_avatar(m["role"])):
            st.markdown(m["content"])

    if soru := st.chat_input("Buraya yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user", avatar=get_avatar("user")):
            st.markdown(soru)
        
        with st.chat_message("assistant", avatar=get_avatar("assistant")):
            try:
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
                with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.mesajlar, f, ensure_ascii=False)
            except Exception as e:
                st.error(f"Hata (Kota Dolmuş Olabilir): {e}")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.info(f"Yazılım Sahibi ve Geliştirici: **Kutay Tatlıcak**")
    st.write("Sürüm: v27.0 Ultimate")
    if st.button("🗑️ Tüm Geçmişi Temizle"):
        for f in os.listdir(KAYIT_YOLU): os.remove(os.path.join(KAYIT_YOLU, f))
        st.success("Hafıza sıfırlandı!")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Lisans ve Haklar")
    st.markdown(f"""
    ### 🛡️ KUTAY AI Resmi Lisansı
    1. **Mülkiyet:** Bu yazılımın tüm hakları **Kutay Tatlıcak**'a aittir.
    2. **Kullanım:** İzinsiz kopyalanması, kaynak kodlarının çalınması ve isimsiz paylaşılması yasaktır.
    3. **Veri:** Kişisel verileriniz ve sohbetleriniz sadece sizin cihazınızda saklanır.
    4. **Sorumluluk:** Yapay zeka yanıtlarından geliştirici sorumlu tutulamaz.
    
    **© 2026 Kutay Tatlıcak. Tüm Hakları Saklıdır.**
    """)
