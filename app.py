import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="KUTAY AI v3.0", page_icon="💎", layout="wide")

# Senin paylaştığın API Anahtarı
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

try:
    genai.configure(api_key=API_KEY)
    # Hata aldığın görselde gemini-1.5-flash kullanıldığı görülüyor, en hızlısı budur.
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Hatası: {e}")

# --- 2. Gelişmiş Görsel Tasarım (O Sevdiğin Eski Hava) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Yan Menü (Sidebar) */
    [data-testid="stSidebar"] { 
        background-color: #161b22; 
        border-right: 2px solid #00d2ff; 
    }

    /* Konuşma Balonları Tasarımı (image_456442.png'deki gibi) */
    .stChatMessage {
        background-color: #1c232d !important;
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
    }
    
    /* Kullanıcı Mesajı Farklı Renk */
    [data-testid="stChatMessageUser"] {
        background-color: #242c38 !important;
        border-left: 5px solid #00d2ff !important;
    }

    /* AI Mesajı Farklı Renk */
    [data-testid="stChatMessageAssistant"] {
        background-color: #1c232d !important;
        border-left: 5px solid #00ff41 !important;
    }

    /* Başlıklar */
    h1, h2, h3 { color: #00d2ff !important; font-family: 'Courier New', Courier, monospace; }
    
    /* Alt Bilgi */
    .footer { position: fixed; bottom: 10px; width: 100%; text-align: left; color: #888; font-size: 12px; }
    </style>
    <div class="footer">© 2026 Kutay AI Lab | Geliştirici: Yusuf Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Sohbet"

# --- 4. SIDEBAR (YAN MENÜ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80) # Küçük bir AI ikonu
    st.title("KUTAY AI PANEL")
    
    st.markdown("---")
    # Sayfa Seçimi
    choice = st.radio("Menü", ["🤖 Sohbet", "⚙️ Ayarlar", "📚 Sohbet Geçmişi"])
    
    st.markdown("---")
    st.subheader("🌐 Sistem Bağlantısı")
    st.info("Kutay Koruma aktif durumda.")
    # Koruma Linki
    st.link_button("🛡️ KUTAY KORUMA'YA GİT", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Belleği Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA İÇERİĞİ ---

if choice == "🤖 Sohbet":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Özelleştirilen Akıllı Asistan")

    # Mesajları Göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Mesaj Girişi
    if prompt := st.chat_input("Yusuf'un yapay zekasına bir şeyler yaz..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            status = st.empty()
            full_response = ""
            
            try:
                # Yapay Zeka Yanıtı
                response = model.generate_content(prompt)
                
                # Akıcı Yazı Efekti
                for chunk in response.text.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    status.markdown(full_response + "▌")
                
                status.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                # 429 KOTA HATASI DÜZENLEMESİ
                if "429" in str(e) or "quota" in str(e).lower():
                    st.error("🚨 KOTA DOLDU: Yusuf, Google ücretsiz limiti doldu. 1 dakika bekleyip tekrar yazarsan düzelecek!")
                else:
                    st.error(f"Bir aksaklık oldu: {e}")

elif choice == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.subheader("Geliştirici Hakları")
    st.markdown("""
    - **Yazılım:** KUTAY AI Legacy Edition
    - **Sürüm:** 3.0 (Stabil)
    - **Geliştirici:** Yusuf Tatlıcak
    - **Telif:** © 2026 Yusuf Tatlıcak Cyber Lab. Tüm hakları saklıdır.
    """)
    st.divider()
    st.write("Sistem Durumu: **Çevrimiçi**")
    st.write("API Modeli: **Gemini 1.5 Flash**")
    st.success("Tüm sistemler optimize edildi.")

elif choice == "📚 Sohbet Geçmişi":
    st.title("📚 Sohbet Geçmişi")
    if not st.session_state.messages:
        st.write("Henüz bir konuşma geçmişi yok.")
    else:
        for idx, msg in enumerate(st.session_state.messages):
            role = "Siz" if msg["role"] == "user" else "KUTAY AI"
            st.text_area(f"{idx+1}. Mesaj ({role})", value=msg["content"], height=100, disabled=True)
