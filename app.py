import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="KUTAY AI PRO", page_icon="💎", layout="centered")

# SENİN YENİ VE AKTİF API ANAHTARIN
API_KEY = "AIzaSyAi-jLhZ8ehae5ZH2HjpB_pI6pllsyU27k"

@st.cache_resource
def setup_engine():
    try:
        genai.configure(api_key=API_KEY)
        # Hata vermemesi için en stabil modeli otomatik seçer
        models = genai.list_models()
        target = next((m.name for m in models if 'gemini-1.5-flash' in m.name), 'models/gemini-1.5-flash')
        return genai.GenerativeModel(model_name=target)
    except Exception as e:
        return f"Sistem Hatası: {e}"

model_engine = setup_engine()

# --- 2. GÖRSEL TASARIM (BEYAZLIKLARI KALDIRILMIŞ TİTİZ TEMA) ---
st.markdown("""
    <style>
    /* ANA EKRAN VE SIDEBAR TAM BEYAZ */
    .stApp, [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
    }
    
    /* YAZILARIN ÜSTÜNDEKİ O GEREKSİZ BEYAZLIĞI/GÖLGEYİ KALDIRAN KOD */
    .stChatMessage { 
        background-color: transparent !important; 
        border-radius: 0px !important; 
        box-shadow: none !important; /* Gölgeyi ve beyaz kutuyu siler */
        border: none !important;
        padding: 10px 0px !important;
        margin-bottom: 5px !important;
    }

    /* KULLANICI YAZISI (SOLDA HAFİF MAVİ ÇİZGİ) */
    [data-testid="stChatMessageUser"] {
        border-left: 4px solid #0052CC !important;
        padding-left: 15px !important;
    }

    /* AI YAZISI (SOLDA HAFİF GRİ ÇİZGİ) */
    [data-testid="stChatMessageAssistant"] {
        border-left: 4px solid #E2E8F0 !important;
        padding-left: 15px !important;
    }

    /* METİN RENKLERİ VE NETLİK */
    p, span, h1, h2, h3 { color: #1A202C !important; font-family: 'Inter', sans-serif; }

    /* YASAL HAKLAR PANELİ (TAM PROFESYONEL) */
    .legal-box {
        background-color: #ffffff;
        border: 2px solid #1A56DB;
        padding: 30px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOL MENÜ (KUTAY PANEL) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### ⚙️ KUTAY PANEL")
    st.caption("Yusuf Tatlıcak Enterprise")
    st.markdown("---")
    
    menu = st.radio("Sistem Katmanı:", ["💬 Ana Terminal", "⚖️ Yasal Haklarım"])
    
    st.markdown("---")
    st.link_button("🛡️ KORUMA HUB", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    if st.button("🗑️ Belleği Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 4. EKRANLAR ---

if menu == "💬 Ana Terminal":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tescilli Yapay Zeka Motoru")

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Komut bekleniyor..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            msg_placeholder = st.empty()
            full_response = ""
            
            if isinstance(model_engine, str):
                st.error(model_engine)
            else:
                try:
                    response = model_engine.generate_content(prompt)
                    for chunk in response.text.split():
                        full_response += chunk + " "
                        time.sleep(0.04)
                        msg_placeholder.markdown(full_response + "▌")
                    msg_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {e}")

elif menu == "⚖️ Yasal Haklarım":
    st.title("⚖️ Mülkiyet ve Yasal Bildiriler")
    st.markdown(f"""
    <div class="legal-box">
        <h2 style="color:#1A56DB;">📜 RESMİ LİSANS BEYANI</h2>
        <p><b>YAZILIM ADI:</b> KUTAY AI (Professional Edition)</p>
        <p><b>GELİŞTİRİCİ:</b> Yusuf Tatlıcak</p>
        <hr>
        <p>1. Bu yazılımın tüm kaynak kodları, görsel tasarımı ve algoritma mimarisi <b>Yusuf Tatlıcak</b>'ın mülkiyetindedir.</p>
        <p>2. Yusuf Tatlıcak'ın yazılı onayı olmadan kodların kopyalanması, değiştirilmesi veya GitHub gibi platformlarda "açık kaynak" adı altında paylaşılması kesinlikle yasaktır.</p>
        <p>3. Yazılım üzerinde tersine mühendislik yapılması veya isminin değiştirilerek kullanılması durumunda yasal işlem başlatma hakkı saklı tutulur.</p>
        <p style="text-align:center; font-weight:bold; color:#1A56DB; margin-top:20px;">🛡️ 2026 Yusuf Tatlıcak Cyber Lab - Her Hakkı Saklıdır.</p>
    </div>
    """, unsafe_allow_html=True)
