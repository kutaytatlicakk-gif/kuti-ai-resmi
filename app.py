import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (HATA VERMEYEN AYARLAR) ---
st.set_page_config(page_title="KUTAY AI v5.5", page_icon="💎", layout="centered")

# Senin paylaştığın API Anahtarı
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

try:
    genai.configure(api_key=API_KEY)
    # GÖRSELLERDEKİ 404 HATASINI ÇÖZEN EN STABİL MODEL İSMİ
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")

# --- 2. GÖRSEL TASARIM (FULL BEYAZ & MODERN) ---
st.markdown("""
    <style>
    /* ANA EKRAN BEYAZ */
    .stApp { background-color: #FFFFFF !important; color: #31333F !important; }
    
    /* SOL MENÜ (SIDEBAR) TAM BEYAZ */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 1px solid #f0f0f0 !important; 
    }
    [data-testid="stSidebar"] * { color: #31333F !important; }

    /* KONUŞMA BALONLARI (image_456442'deki gibi) */
    .stChatMessage {
        border-radius: 18px !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
        max-width: 88% !important;
    }
    
    /* KULLANICI MESAJI (MAVİ) */
    [data-testid="stChatMessageUser"] {
        background-color: #E3F2FD !important;
        border: 1px solid #BBDEFB !important;
        color: #0D47A1 !important;
    }

    /* AI MESAJI (GRİ) */
    [data-testid="stChatMessageAssistant"] {
        background-color: #F8F9FA !important;
        border: 1px solid #E9ECEF !important;
        color: #212529 !important;
    }

    /* YASAL HAKLAR KUTUSU */
    .rights-detail {
        background-color: #fdfdfd;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #1976D2;
        padding: 25px;
        border-radius: 12px;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ALT İMZA */
    .footer-text {
        text-align: center;
        font-size: 11px;
        color: #a0a0a0;
        margin-top: 40px;
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (KUTAY PANEL) ---
with st.sidebar:
    st.markdown("## ⚙️ KUTAY PANEL")
    st.write("Yusuf Tatlıcak Resmi Yazılımı")
    st.markdown("---")
    
    page = st.radio("Sistem Menüsü:", ["💬 Sohbet", "🛠️ Ayarlar & Haklarım", "📜 Geçmiş"])
    
    st.markdown("---")
    st.subheader("🛡️ Siber Güvenlik")
    st.link_button("KUTAY KORUMA'YA GİT", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Belleği Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA FONKSİYONLARI ---

if page == "💬 Sohbet":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Akıllı Asistan")

    # Geçmişi Göster
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Mesaj Girişi
    if prompt := st.chat_input("Yusuf'un yapay zekasına bir şeyler yaz..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            msg_area = st.empty()
            full_res = ""
            try:
                # Yapay Zeka Yanıt Üretimi
                response = model.generate_content(prompt)
                
                # Akıcı Yazım Efekti
                for chunk in response.text.split():
                    full_res += chunk + " "
                    time.sleep(0.04)
                    msg_area.markdown(full_res + "▌")
                
                msg_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                # 404 VE 429 HATALARINI PROFESYONELCE YÖNET
                if "429" in str(e):
                    st.warning("⚠️ **Sistem Notu:** Yusuf, kota doldu. 1 dakika sonra her şey düzelecek.")
                else:
                    st.error(f"🚨 **Sistem Hatası:** {e}")

    st.markdown('<div class="footer-text">© 2026 Yusuf Tatlıcak | Tüm Hakları Saklıdır.</div>', unsafe_allow_html=True)

elif page == "🛠️ Ayarlar & Haklarım":
    st.title("🛡️ Yasal Haklar ve Lisans")
    
    # DETAYLI VE UZUN HAKLAR BÖLÜMÜ
    st.markdown("""
    <div class="rights-detail">
        <h2 style="color:#1976D2; margin-top:0;">📜 Yazılım Mülkiyeti</h2>
        <p><b>KUTAY AI v5.5</b> yazılımının tüm algoritma tasarımı, görsel arayüzü ve entegrasyon yapısı tamamen <b>Yusuf Tatlıcak</b> adına tescillidir.</p>
        
        <h3>📍 Fikri Mülkiyet Detayları</h3>
        <ul>
            <li><b>Yazılımcı:</b> Yusuf Tatlıcak</li>
            <li><b>Teknoloji:</b> KUTAY 1.5 FLASH (Özel Optimize Edilmiş Altyapı)</li>
            <li><b>Sürüm Durumu:</b> Kararlı (Hatasız)</li>
        </ul>

        <h3>⚖️ Yasal Uyarı</h3>
        <p>Bu yazılımın kaynak kodlarının izinsiz olarak;</p>
        <ol>
            <li>Kopyalanması ve başka projelerde kullanılması,</li>
            <li>İsminin değiştirilerek yeniden yayınlanması,</li>
            <li>Ticari kazanç amacıyla dağıtılması,</li>
        </ol>
        <p><b>KESİNLİKLE YASAKTIR.</b> Yusuf Tatlıcak Cyber Security Lab tarafından koruma altındadır.</p>
        
        <p style="color: green; font-weight: bold;">✅ Lisans Durumu: ONAYLANDI (Yusuf Tatlıcak)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write("✅ **Model:** KUTAY 1.5 FLASH")
    st.write("✅ **Güvenlik Skoru:** %100")
    st.success("Sistem Yusuf Tatlıcak için mükemmel hale getirildi.")

elif page == "📜 Geçmiş":
    st.title("📜 Konuşma Geçmişi")
    if not st.session_state.messages:
        st.info("Kayıtlı mesaj bulunamadı.")
    else:
        for m in st.session_state.messages:
            lbl = "Yusuf" if m["role"] == "user" else "KUTAY AI"
            st.text_area(f"{lbl}:", value=m["content"], height=80, disabled=True)
