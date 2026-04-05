import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM VE SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="KUTAY AI v5.2", page_icon="💎", layout="centered")

# API Anahtarın
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")

# --- 2. GÖRSEL TASARIM (BEYAZ TEMA & ÖZEL HAKLAR BÖLÜMÜ) ---
st.markdown("""
    <style>
    /* ANA ARKA PLAN BEYAZ */
    .stApp { background-color: #FFFFFF !important; color: #31333F !important; }
    
    /* SOL MENÜ (SIDEBAR) BEYAZ */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 1px solid #eeeeee !important; 
    }
    [data-testid="stSidebar"] * { color: #31333F !important; }

    /* KONUŞMA BALONLARI */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 12px 18px !important;
        margin-bottom: 10px !important;
        max-width: 85% !important;
    }
    
    /* KULLANICI MESAJI: MAVİ */
    [data-testid="stChatMessageUser"] {
        background-color: #E3F2FD !important;
        border: 1px solid #BBDEFB !important;
        color: #0D47A1 !important;
    }

    /* AI MESAJI: GRİ */
    [data-testid="stChatMessageAssistant"] {
        background-color: #F5F5F5 !important;
        border: 1px solid #E0E0E0 !important;
        color: #212121 !important;
    }

    /* ÖZEL HAKLAR KUTUSU (AYARLARDA GÖRÜNECEK) */
    .rights-box {
        background-color: #f8f9fa;
        border-left: 5px solid #1976D2;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }

    /* ALT BİLGİ İMZASI */
    .footer-stamp {
        text-align: center;
        font-size: 12px;
        color: #bdc3c7;
        margin-top: 50px;
        border-top: 1px solid #eee;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (KUTAY PANEL) ---
with st.sidebar:
    st.markdown("# ⚙️ KUTAY PANEL")
    st.write("Yusuf Tatlıcak Resmi Yazılımı")
    st.markdown("---")
    
    page = st.radio("Menü Seçenekleri:", ["💬 Sohbet", "🛠️ Ayarlar & Haklarım", "📜 Geçmiş"])
    
    st.markdown("---")
    st.subheader("🛡️ Siber Güvenlik")
    st.link_button("KUTAY KORUMA'YA GİT", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 5. SAYFA İÇERİKLERİ ---

if page == "💬 Sohbet":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Akıllı Asistan")

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Yusuf'un yapay zekasına bir şeyler yaz..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            msg_area = st.empty()
            full_res = ""
            try:
                response = model.generate_content(prompt)
                for chunk in response.text.split():
                    full_res += chunk + " "
                    time.sleep(0.04)
                    msg_area.markdown(full_res + "▌")
                msg_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                if "429" in str(e):
                    st.warning("🚨 **SİSTEM NOTU:** Kota doldu Yusuf. 1 dakika bekleyince sistem otomatik açılacaktır.")
                else:
                    st.error(f"Sistem Hatası: {e}")

    # Sayfa sonu imzası
    st.markdown('<div class="footer-stamp">© 2026 Yusuf Tatlıcak | Tüm Hakları Saklıdır.</div>', unsafe_allow_html=True)

elif page == "🛠️ Ayarlar & Haklarım":
    st.title("🛠️ Sistem ve Yasal Haklar")
    
    # Hakların Yazdığı Bölüm
    st.markdown(f"""
    <div class="rights-box">
        <h3 style="color:#1976D2; margin-top:0;">📜 Yazılım ve Telif Hakları</h3>
        <p>Bu yapay zeka yazılımı (KUTAY AI), <b>Yusuf Tatlıcak</b> tarafından geliştirilmiştir.</p>
        <ul>
            <li><b>Geliştirici:</b> Yusuf Tatlıcak</li>
            <li><b>Yazılım Versiyonu:</b> 5.2 (Kararlı Sürüm)</li>
            <li><b>Kullanılan Model:</b> KUTAY 1.5 FLASH</li>
            <li><b>Lisans:</b> Kişisel ve Korunan Yazılım Hakları</li>
        </ul>
        <p style="font-size:13px; color:#666;">Bu yazılımın kaynak kodlarının izinsiz kopyalanması, paylaşılması veya ticari amaçla kullanılması durumunda tüm yasal haklar saklı tutulur.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write("✅ **Model Durumu:** Aktif (**KUTAY 1.5 FLASH**)")
    st.write("✅ **Görünüm:** Beyaz Tema (Modern)")
    st.success("Sistem Yusuf Tatlıcak adına optimize edildi.")

elif page == "📜 Geçmiş":
    st.title("📜 Konuşma Geçmişi")
    if not st.session_state.messages:
        st.info("Henüz bir konuşma kaydı bulunmuyor.")
    else:
        for m in st.session_state.messages:
            label = "Yusuf" if m["role"] == "user" else "KUTAY AI"
            st.text_area(f"{label}:", value=m["content"], height=70, disabled=True)
