import streamlit as st
import google.generativeai as genai
import time
import os

# --- 1. SİSTEM YAPILANDIRMASI (HATA ÖNLEYİCİ) ---
st.set_page_config(page_title="KUTAY AI Professional", page_icon="💎", layout="centered")

# Senin aktif API Anahtarın
API_KEY = "AIzaSyAYeaejVesg2ik5ESyUdQFvyYHwW4ISg_I"

# KRİTİK DÜZELTME: Kütüphanenin v1beta hatasını zorla engellemek için doğrudan configure ediyoruz
try:
    genai.configure(api_key=API_KEY)
    # Model ismini sadece 'gemini-1.5-flash' olarak tanımlıyoruz (v1beta hatasını çözen yöntem)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")

# --- 2. GÖRSEL TASARIM (BEYAZ TEMA & PROFESYONEL UI) ---
st.markdown("""
    <style>
    /* ANA EKRAN BEYAZ */
    .stApp { background-color: #FFFFFF !important; color: #1E1E1E !important; }
    
    /* SOL MENÜ (SIDEBAR) TAM BEYAZ */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 2px solid #f0f2f6 !important; 
    }
    [data-testid="stSidebar"] * { color: #31333F !important; }

    /* KONUŞMA BALONLARI */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px 20px !important;
        margin-bottom: 12px !important;
        max-width: 85% !important;
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

    /* ÇOK DETAYLI HAKLAR PANELİ */
    .legal-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 10px solid #1976D2;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .footer-stamp {
        text-align: center;
        font-size: 13px;
        color: #A0AEC0;
        padding-top: 30px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (KUTAY PANEL) ---
with st.sidebar:
    st.markdown("## ⚙️ KUTAY PANEL")
    st.caption("Yusuf Tatlıcak Özel Geliştirme")
    st.markdown("---")
    
    page = st.radio("Sistem Katmanları:", ["💬 Ana Terminal", "⚖️ Yasal Haklar & Mülkiyet", "📜 Arşiv"])
    
    st.markdown("---")
    st.subheader("🛡️ Güvenlik Merkezi")
    st.link_button("🛡️ KUTAY KORUMA HUB", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Belleği Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA İŞLEMLERİ ---

if page == "💬 Ana Terminal":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Tarafından Geliştirilen Yüksek Performanslı Asistan")

    # Geçmişi Göster
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Mesaj Girişi
    if prompt := st.chat_input("Sisteme komut ver..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            msg_area = st.empty()
            full_res = ""
            
            try:
                # Yanıt Üretme (Hata Kontrolü ile)
                response = model.generate_content(prompt)
                
                # Yazma Efekti
                for word in response.text.split():
                    full_res += word + " "
                    time.sleep(0.04)
                    msg_area.markdown(full_res + "▌")
                
                msg_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

            except Exception as e:
                # 404/429 Hatalarını Yakala ve Yusuf'a Şık Göster
                error_str = str(e)
                if "429" in error_str:
                    st.warning("⚠️ **HIZ SINIRI:** Yusuf, Google kotası doldu. 1 dakika bekle düzelecek.")
                elif "404" in error_str:
                    st.error("🚨 **MODEL HATASI:** Google sunucuları model ismini tanıyamadı. Lütfen API sayfanı yenile veya başka bir API key dene.")
                else:
                    st.error(f"Sistem Hatası: {e}")

    st.markdown('<div class="footer-stamp">© 2026 Yusuf Tatlıcak Cyber Lab | Tüm Hakları Saklıdır.</div>', unsafe_allow_html=True)

elif page == "⚖️ Yasal Haklar & Mülkiyet":
    st.title("🛡️ Resmi Mülkiyet Bildirisi")
    
    st.markdown("""
    <div class="legal-box">
        <h2 style="color:#1976D2; margin-top:0;">📜 Yazılım Lisans Sözleşmesi</h2>
        <p><b>KUTAY AI v6.5</b> yazılımı, tüm algoritmik yapısı ve tasarım hatlarıyla münhasıran <b>Yusuf Tatlıcak</b> adına tescillidir.</p>
        
        <h3>1. Fikri Mülkiyet Hakları</h3>
        <p>Bu uygulama; özel Python mimarisi, CSS3 stil yapılandırmaları ve yapay zeka entegrasyonu kullanılarak Yusuf Tatlıcak tarafından geliştirilmiştir. Kaynak kodlarının tamamı Yusuf Tatlıcak'ın mülkiyetindedir.</p>

        <h3>2. Yasaklar ve Kısıtlamalar</h3>
        <ul>
            <li>Bu yazılımın kodlarının Yusuf Tatlıcak'ın yazılı onayı olmadan kopyalanması, dağıtılması veya üzerinde değişiklik yapılması kesinlikle yasaktır.</li>
            <li>"KUTAY AI" markasının ticari amaçla kullanılması yasal takibat sebebidir.</li>
        </ul>

        <h3>3. Teknik Motor Bilgisi</h3>
        <p>Sistem, <b>KUTAY 1.5 FLASH</b> motoru üzerinden saniyede binlerce veriyi işleyebilen özel bir çekirdek yapısına sahiptir.</p>
        
        <p style="background-color: #f1f8ff; padding: 15px; border-radius: 10px; color: #0052cc; font-weight: bold; text-align: center; border: 1px solid #c2e0ff;">
            🛡️ Yusuf Tatlıcak Cyber Security Lab Tarafından Koruma Altındadır.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write("✅ **Model Altyapısı:** KUTAY 1.5 FLASH")
    st.write("✅ **Telif Sahibi:** Yusuf Tatlıcak")
    st.success("Sistem %100 Yusuf Tatlıcak Standartlarına Uygun.")

elif page == "📜 Arşiv":
    st.title("📜 Konuşma Geçmişi")
    if not st.session_state.messages:
        st.info("Kayıtlı mesaj bulunamadı.")
    else:
        for m in st.session_state.messages:
            lbl = "User" if m["role"] == "user" else "AI"
            st.text_area(f"{lbl}:", value=m["content"], height=80, disabled=True)
