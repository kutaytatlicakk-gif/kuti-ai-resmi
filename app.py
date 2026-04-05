import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (HATA ÖNLEYİCİ MİMARİ) ---
st.set_page_config(page_title="KUTAY AI v10.0", page_icon="💎", layout="centered")

@st.cache_resource
def setup_professional_system():
    try:
        # SECRETS PANELİNDEN ANAHTARI ÇEK
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            return "HATA: Secrets panelinde 'GEMINI_API_KEY' bulunamadı!"

        genai.configure(api_key=api_key)
        
        # 404 HATASINI BİTİREN "LAZER" YÖNTEM:
        # Sunucunun kabul ettiği gerçek isimleri listele ve 'flash' olanı doğrudan yakala
        models = genai.list_models()
        target_name = next((m.name for m in models if 'gemini-1.5-flash' in m.name), None)
        
        if not target_name:
            target_name = 'gemini-1.5-flash' # Manuel yedek
            
        return genai.GenerativeModel(model_name=target_name)
    except Exception as e:
        return f"Sistem Başlatma Hatası: {e}"

model = setup_professional_system()

# --- 2. GÖRSEL TASARIM (BEYAZ TEMA & PREMIUM UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; color: #1A202C !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    [data-testid="stSidebar"] * { color: #2D3748 !important; }
    
    .stChatMessage { border-radius: 20px !important; margin-bottom: 15px !important; }
    [data-testid="stChatMessageUser"] { background-color: #F0F7FF !important; border: 1px solid #E1EFFE !important; color: #1C64F2 !important; }
    [data-testid="stChatMessageAssistant"] { background-color: #F9FAFB !important; border: 1px solid #F3F4F6 !important; color: #374151 !important; }

    .legal-container {
        background-color: #ffffff; border: 1px solid #E2E8F0; border-left: 12px solid #1A56DB;
        padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOL MENÜ ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("## ⚙️ KUTAY PANEL")
    st.caption("Yusuf Tatlıcak Enterprise Edition")
    st.markdown("---")
    page = st.radio("Sistem Katmanları:", ["💬 Ana Terminal", "⚖️ Yasal Haklarım", "📜 Arşiv"])
    st.markdown("---")
    st.link_button("🛡️ KUTAY KORUMA HUB", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    if st.button("🗑️ Verileri Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ANA SAYFA ---
if page == "💬 Ana Terminal":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Yüksek Performanslı Model")

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Sisteme komut ver..."):
        with st.chat_message("user", avatar="👤"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            placeholder = st.empty()
            full_res = ""
            if isinstance(model, str):
                st.error(model)
            else:
                try:
                    response = model.generate_content(prompt)
                    for word in response.text.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"Kritik Hata: {e}")

elif page == "⚖️ Yasal Haklarım":
    st.title("⚖️ Mülkiyet ve Yasal Beyanlar")
    st.markdown("""
    <div class="legal-container">
        <h2 style="color:#1A56DB;">📜 Yazılım Lisans Sözleşmesi</h2>
        <p><b>KUTAY AI v10.0</b> yazılımının tüm fikri hakları münhasıran <b>Yusuf Tatlıcak</b> adına tescillidir.</p>
        <h3>1. Fikri Mülkiyet Koruması</h3>
        <p>Uygulamanın kaynak kodları, CSS3 tasarım mimarisi ve Yusuf Tatlıcak tarafından optimize edilen AI motoru uluslararası telif kanunlarıyla korunmaktadır.</p>
        <h3>2. Kesin Yasaklar</h3>
        <ul>
            <li>Kodların Yusuf Tatlıcak'ın yazılı izni olmadan dağıtılması ve kopyalanması kesinlikle yasaktır.</li>
            <li>"KUTAY AI" markasının izinsiz kullanımı yasal takibat sebebidir.</li>
        </ul>
        <p style="text-align:center; font-weight:bold; color:#1A56DB;">🛡️ 2026 Yusuf Tatlıcak Cyber Lab - Her Hakkı Saklıdır.</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "📜 Arşiv":
    st.title("📜 Sistem Arşivi")
    for m in st.session_state.messages:
        st.text_area(f"{'Yusuf' if m['role']=='user' else 'AI'}:", value=m["content"], height=80, disabled=True)
