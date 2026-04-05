import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM VE SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="KUTAY AI", page_icon="🤖", layout="centered")

# API Anahtarın (Senin paylaştığın aktif anahtar)
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

try:
    genai.configure(api_key=API_KEY)
    # 404 Hatasını önlemek için en stabil model olan gemini-pro kullanıldı
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# --- 2. GÖRSEL TASARIM (BEYAZ ARKA PLAN VE MAVİ BALONLAR) ---
st.markdown("""
    <style>
    /* Ana Arka Planı Beyaz Yap */
    .stApp { background-color: #FFFFFF !important; color: #31333F !important; }
    
    /* Yan Menü (Sidebar) Koyu Kalsın (Kontrast İçin) */
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #ddd; }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Konuşma Balonları Tasarımı (image_456442.png stili) */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 10px 15px !important;
        margin-bottom: 10px !important;
        max-width: 85% !important;
    }
    
    /* Kullanıcı Mesajı: MAVİ ARKA PLAN */
    [data-testid="stChatMessageUser"] {
        background-color: #E1F5FE !important; /* Açık Mavi */
        border: 1px solid #B3E5FC !important;
        float: right !important;
        color: #01579B !important;
    }

    /* Yapay Zeka Mesajı: BEYAZ/GRİ ARKA PLAN */
    [data-testid="stChatMessageAssistant"] {
        background-color: #F8F9FA !important;
        border: 1px solid #E9ECEF !important;
        float: left !important;
        color: #212529 !important;
    }

    /* Başlıklar */
    h1 { color: #007BFF !important; text-align: center; font-weight: 800; }
    
    /* Input Alanı (Yazı Yazma Kısmı) */
    .stChatInputContainer { background-color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI VE SAYFA YÖNETİMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🤖 KUTAY PANEL")
    st.markdown("---")
    
    # Menü Seçenekleri
    page = st.radio("Menüden Seçim Yap:", ["💬 Sohbet", "⚙️ Ayarlar", "📜 Geçmiş"])
    
    st.markdown("---")
    st.subheader("🛡️ Güvenlik Merkezi")
    st.write("Dosya tarama sistemine git:")
    st.link_button("KUTAY KORUMA'YA GİT", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA İÇERİĞİ ---

if page == "💬 Sohbet":
    st.title("🤖 KUTAY AI")
    st.markdown("<p style='text-align: center; color: gray;'>Yusuf Tatlıcak Tarafından Geliştirilen Özel Asistan</p>", unsafe_allow_html=True)

    # Sohbet Geçmişini Ekrana Bas
    for message in st.session_state.messages:
        # Avatarları image_456442.png'ye uygun seçtik
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Kullanıcıdan Yazı Al
    if prompt := st.chat_input("Mesajınızı buraya yazın..."):
        # Kullanıcı mesajını göster ve kaydet
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI Yanıtı
        with st.chat_message("assistant", avatar="💎"):
            msg_area = st.empty()
            full_res = ""
            
            try:
                response = model.generate_content(prompt)
                
                # Yazıyor efekti
                for word in response.text.split():
                    full_res += word + " "
                    time.sleep(0.04)
                    msg_area.markdown(full_res + "▌")
                
                msg_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

            except Exception as e:
                # 429 ve diğer hataları yönet
                if "429" in str(e):
                    st.error("🚨 KOTA DOLDU: Yusuf, Google limiti doldu. 1 dakika bekleyip tekrar yazarsan düzelecek!")
                else:
                    st.error(f"Bir aksaklık oldu: {e}")

elif page == "⚙️ Ayarlar":
    st.title("⚙️ Ayarlar")
    st.info("Sistem Yusuf Tatlıcak adına lisanslanmıştır.")
    st.write("**Model:** Gemini Pro (Stabil)")
    st.write("**Versiyon:** 4.0 (Legacy Modern)")
    st.write("**Tema:** Aydınlık Mod (Aktif)")
    st.success("Tüm sistemler stabil çalışıyor.")

elif page == "📜 Geçmiş":
    st.title("📜 Konuşma Geçmişi")
    if not st.session_state.messages:
        st.warning("Henüz bir konuşma kaydı yok.")
    else:
        for m in st.session_state.messages:
            role_name = "Siz" if m["role"] == "user" else "KUTAY AI"
            st.text_area(f"{role_name}:", value=m["content"], height=80, disabled=True)
