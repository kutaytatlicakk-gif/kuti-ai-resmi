import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KutiAİ Pro", page_icon="⚡", layout="centered")

# --- GELİŞMİŞ ŞİFRE KONTROLÜ ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets.get("ACCESS_PASSWORD", "12345"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🛡️ KutiAİ Sistem Güvenliği")
        st.text_input("Giriş Şifresini Girin:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Hatalı Şifre! Tekrar Deneyin:", type="password", on_change=password_entered, key="password")
        st.error("Erişim Engellendi.")
        return False
    return True

# --- ANA SİSTEM ---
if check_password():
    st.title("🤖 KutiAİ v14.0 - Profesyonel Sürüm")
    st.caption("Bağlantı: Şifreli | Durum: Çevrimiçi | Güvenlik: Maksimum")

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Sistem Hatası: API Anahtarı eksik. Lütfen Streamlit Secrets kısmına ekleyin.")
        st.stop()

    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    # PRO ÇÖZÜM: 404 Hatasını %100 Engelleyen Dinamik Seçici
    @st.cache_resource
    def load_model():
        try:
            # Google'dan hesabına izin verilen güncel modellerin listesini çeker
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Sistem senin anahtarına en uygun ve hatasız modeli otomatik bulur
            if 'models/gemini-1.5-flash' in available_models:
                target = 'gemini-1.5-flash'
            elif 'models/gemini-1.5-pro' in available_models:
                target = 'gemini-1.5-pro'
            elif 'models/gemini-pro' in available_models:
                target = 'gemini-pro'
            else:
                target = available_models[0].replace('models/', '') # Ne bulursa onu kullanır
                
            return genai.GenerativeModel(target)
        except Exception as e:
            st.error(f"Google API Bağlantı Hatası (Anahtar Geçersiz Olabilir): {e}")
            st.stop()

    model = load_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): 
            st.markdown(m["content"])

    if p := st.chat_input("Sisteme komut ver..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): 
            st.markdown(p)
            
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(p)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Kritik Hata Oluştu: {str(e)}")
