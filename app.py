import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="KutiAI v16.0 PRO", page_icon="⚡", layout="wide")

# --- API AYARI ---
API_KEY = "AIzaSyAy4UAzQafV4GmwdNo_w6tS3dmzirD0P4Q"
genai.configure(api_key=API_KEY)

# --- 404 HATASINI KÖKTEN ÇÖZEN OTO-TARAMA MOTORU ---
# Bu sistem Google'a bağlanır ve senin API anahtarının desteklediği modeli otomatik bulur.
@st.cache_resource
def en_iyi_modeli_bul():
    try:
        mevcut_modeller = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                mevcut_modeller.append(m.name)
        
        # Eğer sistemde flash veya pro varsa öncelikle onları seç
        for model_adi in mevcut_modeller:
            if "flash" in model_adi or "pro" in model_adi:
                return model_adi
                
        # Bulamazsa listedeki ilk çalışan modeli seç
        return mevcut_modeller[0] if mevcut_modeller else "gemini-1.0-pro"
    except Exception:
        return "gemini-1.0-pro"

# Modeli sisteme yükle (Artık isim sallamıyoruz, sistem kendi buluyor)
aktif_model_adi = en_iyi_modeli_bul()
model = genai.GenerativeModel(aktif_model_adi)

# --- HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN PANEL TASARIMI ---
with st.sidebar:
    st.title("⚡ KUTI-AI PRO")
    st.success("Sistem: Oto-Tarama Aktif")
    
    # Sistemin hangi modeli bulduğunu yan panelde havalı bir şekilde gösterelim
    temiz_isim = aktif_model_adi.replace('models/', '')
    st.info(f"Bağlanan Model:\n{temiz_isim}")
    
    st.markdown("---")
    if st.button("🗑️ Sohbeti Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN TASARIMI ---
st.title("🤖 KutiAI Siber Asistan")
st.caption("Yusuf'un Özel Yapay Zekası | Dinamik API Bağlantısı")
st.markdown("---")

# --- SOHBETİ EKRANA YAZDIRMA ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ ---
prompt = st.chat_input("KutiAI'ye komut gönder...")

if prompt:
    # 1. Mesajı ekrana yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Yapay zekadan cevap al
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            ai_cevap = response.text
            st.markdown(ai_cevap)
            st.session_state.messages.append({"role": "assistant", "content": ai_cevap})
        except Exception as e:
            st.error(f"SİSTEM HATASI: {e}")
