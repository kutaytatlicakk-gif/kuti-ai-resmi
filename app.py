import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (HATA VERMEYEN AYARLAR) ---
st.set_page_config(page_title="KUTAY AI v5.6", page_icon="💎", layout="centered")

# Senin paylaştığın API Anahtarı
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

try:
    genai.configure(api_key=API_KEY)
    # GÖRSELLERDEKİ 404 HATASINI ÇÖZEN EN STABİL MODEL TANIMI
    # 'v1beta' hatasını önlemek için doğrudan model ismi kullanıldı
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")

# --- 2. GÖRSEL TASARIM (FULL BEYAZ & MODERN SİSTEM) ---
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

    /* KONUŞMA BALONLARI */
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

    /* ÇOK DETAYLI YASAL HAKLAR KUTUSU */
    .rights-detail {
        background-color: #fdfdfd;
        border: 1px solid #e0e0e0;
        border-left: 8px solid #1976D2;
        padding: 30px;
        border-radius: 15px;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.6;
    }

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
                # HATALARI PROFESYONELCE YÖNET
                if "429" in str(e):
                    st.warning("⚠️ **Sistem Notu:** Yusuf, kota doldu. 1 dakika sonra her şey düzelecek.")
                else:
                    st.error(f"🚨 **Sistem Hatası:** {e}")

    st.markdown('<div class="footer-text">© 2026 Yusuf Tatlıcak | Tüm Hakları Saklıdır.</div>', unsafe_allow_html=True)

elif page == "🛠️ Ayarlar & Haklarım":
    st.title("🛡️ Yasal Haklar, Lisans ve Mülkiyet")
    
    # ÇOK DETAYLI VE UZUN HAKLAR BÖLÜMÜ
    st.markdown("""
    <div class="rights-detail">
        <h2 style="color:#1976D2; margin-top:0;">📜 Resmi Yazılım Lisans Sözleşmesi</h2>
        <p>Bu yapay zeka yazılımı (<b>KUTAY AI v5.6</b>), tüm fikri ve sınai hakları saklı kalmak kaydıyla münhasıran <b>Yusuf Tatlıcak</b> tarafından tasarlanmış ve kodlanmıştır.</p>
        
        <h3>1. Fikri Mülkiyet ve Telif Hakları</h3>
        <p>Uygulamanın kaynak kodları, arayüz tasarımı (UI/UX), veri işleme algoritmaları ve "KUTAY AI" markası uluslararası telif hakları yasalarıyla korunmaktadır. Yazılımın her bir satırı Yusuf Tatlıcak Cyber Security Lab bünyesinde tescillenmiştir.</p>

        <h3>2. Kullanım Koşulları ve Yasaklar</h3>
        <p>Aşağıdaki eylemlerin gerçekleştirilmesi yasal takibat sebebidir:</p>
        <ul>
            <li>Yazılımın "Reverse Engineering" (Tersine Mühendislik) yöntemiyle kodlarının açılması.</li>
            <li>Kaynak kodlarının Yusuf Tatlıcak'ın yazılı izni olmadan GitHub veya diğer platformlarda paylaşılması.</li>
            <li>Yazılım isminin değiştirilerek "kendi yapımım" şeklinde sunulması.</li>
        </ul>

        <h3>3. Teknoloji ve Model Bilgisi</h3>
        <p>Bu sistem, Google Gemini altyapısı üzerine inşa edilmiş <b>KUTAY 1.5 FLASH</b> özel optimizasyon modelini kullanmaktadır.</p>
        
        <p style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; color: #2e7d32; font-weight: bold; text-align: center;">
            ⚖️ 2026 Yusuf Tatlıcak - Tüm Hakları Kanunlar Çerçevesinde Saklıdır.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write("✅ **Model İsmi:** KUTAY 1.5 FLASH")
    st.write("✅ **Lisans Sahibi:** Yusuf Tatlıcak")
    st.success("Sistem Yusuf Tatlıcak için %100 kararlı hale getirildi.")

elif page == "📜 Geçmiş":
    st.title("📜 Konuşma Geçmişi")
    if not st.session_state.messages:
        st.info("Henüz bir kayıt yok.")
    else:
        for m in st.session_state.messages:
            lbl = "Yusuf" if m["role"] == "user" else "KUTAY AI"
            st.text_area(f"{lbl}:", value=m["content"], height=80, disabled=True)
