import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (HATA ÖNLEYİCİ) ---
st.set_page_config(page_title="KUTAY AI v9.5", page_icon="💎", layout="centered")

@st.cache_resource
def setup_professional_system():
    try:
        # SECRETS KONTROLÜ
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        else:
            return "HATA: Streamlit Secrets panelinde 'GEMINI_API_KEY' bulunamadı!"

        genai.configure(api_key=api_key)
        
        # 404 HATASINI BİTİREN DİNAMİK MODEL SEÇİCİ
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        target = None
        for m in available_models:
            if 'gemini-1.5-flash' in m:
                target = m
                break
        
        if not target:
            target = 'models/gemini-1.5-flash'
            
        return genai.GenerativeModel(model_name=target)
    except Exception as e:
        return f"Sistem Başlatma Hatası: {e}"

model = setup_professional_system()

# --- 2. GÖRSEL TASARIM (FULL BEYAZ & PREMIUM UI) ---
st.markdown("""
    <style>
    /* ANA EKRAN BEYAZLIK AYARI */
    .stApp { background-color: #FFFFFF !important; color: #1E1E1E !important; }
    
    /* SOL MENÜ (SIDEBAR) TAM BEYAZ */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 1px solid #F0F2F6 !important; 
    }
    [data-testid="stSidebar"] * { color: #31333F !important; }

    /* KONUŞMA BALONLARI */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px 20px !important;
        margin-bottom: 12px !important;
        max-width: 85% !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
    }
    
    /* KULLANICI MESAJI: MAVİ */
    [data-testid="stChatMessageUser"] {
        background-color: #EBF5FF !important;
        border: 1px solid #D1E9FF !important;
        color: #0052CC !important;
    }

    /* AI MESAJI: GRİ */
    [data-testid="stChatMessageAssistant"] {
        background-color: #F7F9FB !important;
        border: 1px solid #EDF2F7 !important;
        color: #2D3748 !important;
    }

    /* ULTRA DETAYLI YASAL HAKLAR PANELİ */
    .legal-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 12px solid #1976D2;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        font-family: 'Segoe UI', sans-serif;
    }
    
    .footer-stamp {
        text-align: center;
        font-size: 13px;
        color: #A0AEC0;
        padding-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (KUTAY PANEL) ---
with st.sidebar:
    st.markdown("## ⚙️ KUTAY PANEL")
    st.caption("Yusuf Tatlıcak Enterprise Edition")
    st.markdown("---")
    
    page = st.radio("Sistem Menüsü:", ["💬 Ana Terminal", "⚖️ Detaylı Haklarım", "📜 Arşiv"])
    
    st.markdown("---")
    st.subheader("🛡️ Siber Güvenlik")
    st.link_button("🛡️ KUTAY KORUMA HUB", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Belleği Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA İŞLEMLERİ ---

if page == "💬 Ana Terminal":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Yüksek Performanslı Yapay Zeka")

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Yusuf'un sistemine talimat ver..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            msg_area = st.empty()
            full_res = ""
            
            if isinstance(model, str):
                st.error(model)
            else:
                try:
                    response = model.generate_content(prompt)
                    for word in response.text.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        msg_area.markdown(full_res + "▌")
                    msg_area.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"Sistem Hatası: {e}")

    st.markdown('<div class="footer-stamp">© 2026 Yusuf Tatlıcak Cyber Lab | Tüm Hakları Saklıdır.</div>', unsafe_allow_html=True)

elif page == "⚖️ Detaylı Haklarım":
    st.title("🛡️ Yasal Haklar ve Mülkiyet Bildirisi")
    
    st.markdown("""
    <div class="legal-container">
        <h2 style="color:#1976D2; margin-top:0;">📜 Resmi Yazılım Lisans Sözleşmesi</h2>
        <p>Bu yapay zeka yazılımı (<b>KUTAY AI v9.5</b>), kod mimarisinden görsel tasarımına kadar her detayıyla münhasıran <b>Yusuf Tatlıcak</b> adına tescillenmiştir.</p>
        
        <h3>1. Fikri Mülkiyet Haklarının Korunması</h3>
        <p>Uygulamanın kaynak kodları, CSS3 tabanlı dinamik arayüz mimarisi, kullanıcı deneyimi (UX) tasarımı ve "KUTAY AI" markası, ulusal ve uluslararası fikri mülkiyet kanunları uyarınca Yusuf Tatlıcak'ın mutlak mülkiyetindedir.</p>

        <h3>2. Kullanım Koşulları, Yasaklar ve Cezai Şartlar</h3>
        <p>Aşağıdaki eylemler kesinlikle yasaktır ve yasal takibat sebebidir:</p>
        <ul>
            <li>Bu yazılımın kodlarının Yusuf Tatlıcak'ın yazılı onayı olmadan kopyalanması, GitHub veya benzeri mecralarda paylaşılması.</li>
            <li>Kaynak kodları üzerinde tersine mühendislik yapılması veya "decompile" edilmesi.</li>
            <li>Yazılım isminin değiştirilerek başka birine aitmiş gibi sunulması veya ticari kazanç sağlanması.</li>
        </ul>

        <h3>3. Teknik Motor ve Model Bilgisi</h3>
        <p>Sistem, Yusuf Tatlıcak tarafından optimize edilen <b>KUTAY 1.5 FLASH</b> motoru üzerinden çalışmaktadır. Bu motor, yüksek hız ve doğruluk için özel parametrelerle yapılandırılmıştır.</p>
        
        <p style="background-color: #f1f8ff; padding: 20px; border-radius: 10px; color: #0052cc; font-weight: bold; text-align: center; border: 2px solid #c2e0ff;">
            🛡️ 2026 Yusuf Tatlıcak Cyber Security Lab - Her Hakkı Uluslararası Kanunlarla Saklıdır.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write("✅ **Model İsmi:** KUTAY 1.5 FLASH")
    st.write("✅ **Lisans Sahibi:** Yusuf Tatlıcak")
    st.success("Sistem %100 Yusuf Tatlıcak standartlarına uygun şekilde mühürlendi.")

elif page == "📜 Arşiv":
    st.title("📜 Konuşma Geçmişi")
    if not st.session_state.messages:
        st.info("Kayıtlı mesaj bulunamadı.")
    else:
        for m in st.session_state.messages:
            lbl = "Yusuf" if m["role"] == "user" else "AI"
            st.text_area(f"{lbl}:", value=m["content"], height=80, disabled=True)
