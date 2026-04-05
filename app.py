import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM VE SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="KUTAY AI", page_icon="🤖", layout="centered")

# API Anahtarın
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

try:
    genai.configure(api_key=API_KEY)
    # HATA ÇÖZÜMÜ: v1beta hatalarını önlemek için model ismini güncelledik
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# --- 2. GÖRSEL TASARIM (HER YER BEYAZ VE MODERN) ---
st.markdown("""
    <style>
    /* ANA ARKA PLAN BEYAZ */
    .stApp { background-color: #FFFFFF !important; color: #31333F !important; }
    
    /* SOL MENÜ (SIDEBAR) BEYAZ YAPILDI */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 1px solid #eeeeee !important; 
    }
    [data-testid="stSidebar"] * { color: #31333F !important; }
    
    /* SIDEBAR BUTONLARI VE RADİO DÜZELTME */
    .stRadio > label { color: #31333F !important; font-weight: bold !important; }

    /* KONUŞMA BALONLARI (MAVİ VE GRİ) */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 12px 18px !important;
        margin-bottom: 10px !important;
        max-width: 85% !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* KULLANICI MESAJI: AÇIK MAVİ */
    [data-testid="stChatMessageUser"] {
        background-color: #E3F2FD !important;
        border: 1px solid #BBDEFB !important;
        color: #0D47A1 !important;
    }

    /* AI MESAJI: AÇIK GRİ */
    [data-testid="stChatMessageAssistant"] {
        background-color: #F5F5F5 !important;
        border: 1px solid #E0E0E0 !important;
        color: #212121 !important;
    }

    /* BAŞLIK VE METİNLER */
    h1 { color: #1976D2 !important; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stChatInputContainer { background-color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (SIDEBAR) İÇERİĞİ ---
with st.sidebar:
    st.markdown("# ⚙️ KUTAY PANEL")
    st.write("Yusuf Tatlıcak Özel Sistemi")
    st.markdown("---")
    
    page = st.radio("Menü:", ["💬 Sohbet", "🛠️ Ayarlar", "📜 Geçmiş"])
    
    st.markdown("---")
    st.subheader("🛡️ Güvenlik")
    st.link_button("KUTAY KORUMA'YA GİT", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA EKRAN İŞLEMLERİ ---

if page == "💬 Sohbet":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Akıllı Asistan")

    # Geçmişi Göster
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Mesaj Girişi
    if prompt := st.chat_input("Buraya yazın..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Yanıt Üretme
        with st.chat_message("assistant", avatar="💎"):
            msg_area = st.empty()
            full_res = ""
            
            try:
                # Modeli çağır
                response = model.generate_content(prompt)
                
                # Yazma efekti
                for word in response.text.split():
                    full_res += word + " "
                    time.sleep(0.04)
                    msg_area.markdown(full_res + "▌")
                
                msg_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

            except Exception as e:
                # Hata Yönetimi
                error_msg = str(e)
                if "429" in error_msg:
                    st.warning("⚠️ Kota doldu Yusuf. 30 saniye sonra tekrar dene.")
                elif "404" in error_msg:
                    st.error("🚨 Model ismi güncelleniyor, lütfen sayfayı yenile.")
                else:
                    st.error(f"Sistemde bir hata oluştu: {e}")

elif page == "🛠️ Ayarlar":
    st.title("🛠️ Sistem Ayarları")
    st.success("Yazılım Yusuf Tatlıcak adına tescillidir.")
    st.write("**Versiyon:** 5.0 (Final)")
    st.write("**Görünüm:** Full White Mode")
    st.write("**Model Durumu:** Aktif (Gemini 1.5 Flash)")

elif page == "📜 Geçmiş":
    st.title("📜 Konuşma Kayıtları")
    if not st.session_state.messages:
        st.info("Henüz kayıtlı mesaj yok.")
    else:
        for m in st.session_state.messages:
            label = "Yusuf" if m["role"] == "user" else "AI"
            st.text_area(f"{label}:", value=m["content"], height=70, disabled=True)
