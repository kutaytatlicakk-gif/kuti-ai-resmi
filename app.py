import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM VE API YAPILANDIRMASI ---
st.set_page_config(page_title="KUTAY AI", page_icon="🤖", layout="wide")

# Senin paylaştığın API Anahtarı buraya eklendi
API_KEY = "AIzaSyAi-jLhZ8ehae5ZH2HjpB_pI6pllsyU27k"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# --- 2. GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Yan Menü (Sidebar) */
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 2px solid #3d85f6; }
    
    /* Geliştirici İmzası */
    .dev-footer { position: fixed; bottom: 10px; left: 10px; color: #9ba0a6; font-size: 12px; z-index: 100; }
    
    /* Sohbet Balonları */
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    </style>
    <div class="dev-footer">🤖 KUTAY AI v2.0 | Geliştirici: Yusuf Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 3. YAN MENÜ (PROJE BAĞLANTILARI) ---
with st.sidebar:
    st.title("🛡️ KUTAY LABORATUVARI")
    st.write("Yusuf Tatlıcak'ın yapay zeka ekosistemine hoş geldin.")
    
    st.markdown("---")
    st.subheader("🌐 Güvenlik Merkezi")
    st.info("Dosya veya URL taramak için siber güvenlik sistemime geçebilirsin:")
    
    # Koruma Projenin Linki
    st.link_button("🛡️ KUTAY KORUMA'YA GİT", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("Sohbet Geçmişini Sil"):
        st.session_state.messages = []
        st.rerun()

# --- 4. SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 KUTAY AI")
st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Özel Asistan")

# Mesajları Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Bana bir soru sor..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Yapay Zeka Yanıtı
            response = model.generate_content(prompt)
            
            # Yazma Efekti
            for kelime in response.text.split():
                full_response += kelime + " "
                time.sleep(0.04)
                placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # 429 HATASINI (KOTA) YÖNETEN KISIM
            error_text = str(e)
            if "429" in error_text or "quota" in error_text.lower():
                st.error("🚨 **SİSTEM NOTU:** Yusuf, şu an çok fazla istek gönderildiği için Google kotası doldu. 1-2 dakika bekleyince sistem kendiliğinden düzelecektir.")
            else:
                st.error(f"Sistemde bir aksaklık oldu: {e}")
