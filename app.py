import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (HATA ÖNLEYİCİ) ---
st.set_page_config(page_title="KUTAY AI v6.0 Professional", page_icon="💎", layout="centered")

# API Anahtarı Tanımlama
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

@st.cache_resource
def load_model():
    try:
        genai.configure(api_key=API_KEY)
        # 404 Hatasını çözen kritik satır: v1beta çakışmasını engellemek için model yolu netleştirildi
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        # Model ismini kütüphanenin kabul ettiği en saf haliyle tanımlıyoruz
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=generation_config
        )
        return model
    except Exception as e:
        return f"Sistem Hatası: {e}"

model = load_model()

# --- 2. GÖRSEL TASARIM (GELİŞMİŞ BEYAZ TEMA) ---
st.markdown("""
    <style>
    /* ANA EKRAN BEYAZLIK AYARI */
    .stApp { background-color: #FFFFFF !important; color: #1E1E1E !important; }
    
    /* SOL MENÜ (SIDEBAR) TERTEMİZ BEYAZ */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 2px solid #F0F2F6 !important; 
    }
    [data-testid="stSidebar"] * { color: #31333F !important; }

    /* KONUŞMA BALONLARI (MODERN TASARIM) */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px 20px !important;
        margin-bottom: 15px !important;
        max-width: 85% !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* KULLANICI MESAJI (PROFESYONEL MAVİ) */
    [data-testid="stChatMessageUser"] {
        background-color: #EBF5FF !important;
        border: 1px solid #D1E9FF !important;
        color: #0052CC !important;
    }

    /* AI MESAJI (STİLİZE GRİ) */
    [data-testid="stChatMessageAssistant"] {
        background-color: #F7F9FB !important;
        border: 1px solid #EDF2F7 !important;
        color: #2D3748 !important;
    }

    /* DETAYLI YASAL HAKLAR PANELİ */
    .legal-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 10px solid #1976D2;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* ALT İMZA TASARIMI */
    .footer-stamp {
        text-align: center;
        font-size: 13px;
        color: #A0AEC0;
        padding: 20px;
        letter-spacing: 1px;
    }
    
    /* INPUT ALANI DÜZELTME */
    .stChatInputContainer { background-color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (PROFESYONEL KUTAY PANEL) ---
with st.sidebar:
    st.markdown("## ⚙️ KUTAY PANEL")
    st.caption("Yusuf Tatlıcak Enterprise Edition")
    st.markdown("---")
    
    page = st.radio("Sistem Katmanları:", ["💬 Ana Terminal", "⚖️ Yasal Haklar & Lisans", "📜 Arşiv"])
    
    st.markdown("---")
    st.subheader("🛡️ Siber Güvenlik")
    st.link_button("KUTAY KORUMA HUB", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Verileri Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA FONKSİYONLARI ---

if page == "💬 Ana Terminal":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Yüksek Performanslı Asistan")

    # Sohbet Geçmişi Render
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Mesaj Giriş Mekanizması
    if prompt := st.chat_input("Yusuf'un sistemine talimat ver..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            msg_placeholder = st.empty()
            full_response = ""
            
            if isinstance(model, str): # Model yükleme hatası kontrolü
                st.error(model)
            else:
                try:
                    # YANIT ÜRETİMİ
                    response = model.generate_content(prompt)
                    
                    # Yazma Efekti (Typewriter Effect)
                    for word in response.text.split():
                        full_res = full_response + word + " "
                        full_response = full_res
                        time.sleep(0.04)
                        msg_placeholder.markdown(full_response + "▌")
                    
                    msg_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                except Exception as e:
                    # KRİTİK HATA YÖNETİMİ
                    error_txt = str(e)
                    if "429" in error_txt:
                        st.warning("⚠️ **HIZ SINIRI:** Yusuf, sistem çok yoğun. Lütfen 30 saniye sonra tekrar dene.")
                    else:
                        st.error("🚨 **SİSTEM KRİTİK:** Model bağlantısı kurulamadı. Lütfen API anahtarını veya internet bağlantını kontrol et.")

    st.markdown('<div class="footer-stamp">© 2026 Yusuf Tatlıcak Enterprise | Tüm Hakları Uluslararası Kanunlarla Saklıdır.</div>', unsafe_allow_html=True)

elif page == "⚖️ Yasal Haklar & Lisans":
    st.title("⚖️ Mülkiyet ve Yasal Bildiriler")
    
    st.markdown("""
    <div class="legal-container">
        <h2 style="color:#1976D2; margin-top:0;">📜 Resmi Lisans Bildirisi</h2>
        <p><b>KUTAY AI v6.0</b> yazılımının tüm fikri mülkiyet, tasarım ve uygulama hakları münhasıran <b>Yusuf Tatlıcak</b> şahsına aittir.</p>
        
        <h3>1. Yazılım Mülkiyeti</h3>
        <p>Bu uygulama; özel Python algoritmaları, CSS stil yapılandırmaları ve Google Gemini Pro entegrasyonu kullanılarak Yusuf Tatlıcak tarafından inşa edilmiştir. Kaynak kodlarının tamamı Yusuf Tatlıcak'ın mülkiyetindedir.</p>

        <h3>2. Yasaklar ve Kısıtlamalar</h3>
        <ul>
            <li><b>Kopyalama:</b> Yazılımın herhangi bir parçasının izinsiz kopyalanması ve başka isimlerle yayınlanması yasaktır.</li>
            <li><b>Tersine Mühendislik:</b> Kod yapısının analiz edilmesi veya "decompile" edilmesi kesinlikle yasaktır.</li>
            <li><b>Marka İhlali:</b> "KUTAY AI" ve "KUTAY PANEL" markalarının Yusuf Tatlıcak dışındaki kişilerce ticari amaçla kullanılması yasaktır.</li>
        </ul>

        <h3>3. Teknik Altyapı</h3>
        <p>Sistem, <b>KUTAY 1.5 FLASH</b> motoru ile çalışmaktadır. Bu motor, saniyede binlerce parametreyi işleyebilen özel bir mimariye sahiptir.</p>
        
        <p style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; color: #0d47a1; font-weight: bold; text-align: center; border: 1px solid #bbdefb;">
            🛡️ 2026 - Yusuf Tatlıcak Cyber Security Lab Tarafından Korunmaktadır.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "📜 Arşiv":
    st.title("📜 Sistem Arşivi")
    if not st.session_state.messages:
        st.info("Sistem belleği şu an boş.")
    else:
        for m in st.session_state.messages:
            lbl = "User" if m["role"] == "user" else "KUTAY AI"
            st.text_area(f"Kaynak: {lbl}", value=m["content"], height=100, disabled=True)
