import streamlit as st
import google.generativeai as genai
import time

# --- 1. SİSTEM YAPILANDIRMASI (SIFIR HATA MİMARİSİ) ---
st.set_page_config(page_title="KUTAY AI v11.0", page_icon="💎", layout="centered")

# PROFESYONEL API YÖNETİMİ
# Not: Güvenliğin için bu anahtarı Streamlit Secrets'a koymanı öneririm, 
# ama şimdilik doğrudan çalışması için buraya tanımlıyorum.
API_KEY = "AIzaSyAi-jLhZ8ehae5ZH2HjpB_pI6pllsyU27k"

@st.cache_resource
def setup_professional_engine():
    try:
        genai.configure(api_key=API_KEY)
        
        # DİNAMİK MODEL TARAYICI (404 HATASINI KÖKTEN ÇÖZER)
        # Sunucudaki aktif modelleri sorgular ve en güncel 'flash' versiyonunu seçer.
        models = genai.list_models()
        active_model = next((m.name for m in models if 'gemini-1.5-flash' in m.name), 'models/gemini-1.5-flash')
        
        return genai.GenerativeModel(model_name=active_model)
    except Exception as e:
        return f"🚨 KRİTİK BAĞLANTI HATASI: {str(e)}"

model_engine = setup_professional_engine()

# --- 2. GÖRSEL TASARIM (FULL PREMIUM BEYAZ) ---
st.markdown("""
    <style>
    /* ANA EKRAN BEYAZLIK VE METİN NETLİĞİ */
    .stApp { background-color: #FFFFFF !important; color: #1A202C !important; }
    
    /* SOL MENÜ (SIDEBAR) TASARIMI */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important; 
        border-right: 1px solid #E2E8F0 !important; 
    }
    [data-testid="stSidebar"] * { color: #2D3748 !important; }

    /* KONUŞMA BALONLARI (MODERN VE TİTİZ) */
    .stChatMessage { border-radius: 20px !important; margin-bottom: 15px !important; padding: 18px !important; }
    
    /* KULLANICI MESAJI */
    [data-testid="stChatMessageUser"] { 
        background-color: #F0F7FF !important; 
        border: 1px solid #E1EFFE !important; 
        color: #1C64F2 !important; 
    }

    /* AI MESAJI */
    [data-testid="stChatMessageAssistant"] { 
        background-color: #F9FAFB !important; 
        border: 1px solid #F3F4F6 !important; 
        color: #374151 !important; 
    }

    /* YASAL HAKLAR KONTEYNERI (HUKUKİ GÖRÜNÜM) */
    .legal-container {
        background-color: #ffffff; 
        border: 1px solid #EDF2F7; 
        border-left: 12px solid #1A56DB;
        padding: 45px; 
        border-radius: 15px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        font-family: 'Inter', sans-serif;
    }
    
    .footer-stamp {
        text-align: center;
        font-size: 13px;
        color: #94A3B8;
        margin-top: 50px;
        letter-spacing: 1.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SOL MENÜ (KUTAY KONTROL MERKEZİ) ---
with st.sidebar:
    st.markdown("## ⚙️ KUTAY PANEL")
    st.write("Yusuf Tatlıcak Resmi Yazılımı")
    st.markdown("---")
    
    nav = st.radio("Sistem Katmanları:", ["💬 Ana Terminal", "⚖️ Yasal Haklarım", "📜 Arşiv"])
    
    st.markdown("---")
    st.subheader("🛡️ Siber Güvenlik")
    st.link_button("KUTAY KORUMA HUB", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    
    st.markdown("---")
    if st.button("🗑️ Belleği Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA SAYFA FONKSİYONLARI ---

if nav == "💬 Ana Terminal":
    st.title("🤖 KUTAY AI")
    st.caption("Yusuf Tatlıcak Enterprise Edition | v11.0 Professional")

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "💎"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Yusuf'un sistemine talimat ver..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="💎"):
            placeholder = st.empty()
            full_res = ""
            
            if isinstance(model_engine, str):
                st.error(model_engine)
            else:
                try:
                    # YANIT ÜRETİMİ
                    response = model_engine.generate_content(prompt)
                    
                    # TİTİZ YAZMA EFEKTİ
                    for word in response.text.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                
                except Exception as e:
                    # DETAYLI HATA ANALİZİ
                    err_msg = str(e)
                    if "429" in err_msg:
                        st.warning("⚠️ **KOTA DOLDU:** Yusuf, Google sunucuları çok yoğun. 30 saniye bekle.")
                    elif "400" in err_msg:
                        st.error("🚨 **API HATASI:** Bu anahtar geçersiz olabilir veya süresi dolmuş olabilir.")
                    else:
                        st.error(f"Sistem Hatası: {e}")

    st.markdown('<div class="footer-stamp">© 2026 YUSUF TATLICAK | TÜM HAKLARI ULUSLARARASI KANUNLARLA SAKLIDIR.</div>', unsafe_allow_html=True)

elif nav == "⚖️ Yasal Haklarım":
    st.title("🛡️ Mülkiyet ve Yasal Beyanlar")
    
    st.markdown("""
    <div class="legal-container">
        <h2 style="color:#1A56DB; margin-top:0;">📜 Yazılım Lisans Sözleşmesi</h2>
        <p>Bu yapay zeka yazılımı (<b>KUTAY AI v11.0</b>), kod mimarisinden görsel tasarımına kadar her detayıyla münhasıran <b>Yusuf Tatlıcak</b> adına tescillenmiştir.</p>
        
        <h3>1. Fikri Mülkiyetin Mutlak Korunması</h3>
        <p>Uygulamanın kaynak kodları, Python çekirdek yapısı, CSS3 görsel motoru ve kullanıcı deneyimi (UX) mimarisi Yusuf Tatlıcak'ın fikri emeğidir ve uluslararası telif hakları yasalarıyla korunmaktadır.</p>

        <h3>2. Kullanım Kısıtlamaları ve Ağır Yasaklar</h3>
        <ul>
            <li>Bu yazılımın kodlarının Yusuf Tatlıcak'ın yazılı ve mühürlü onayı olmadan kopyalanması, GitHub'da açık paylaşılması veya dağıtılması kesinlikle yasaktır.</li>
            <li>Kaynak kodları üzerinde tersine mühendislik yapılması veya "decompile" edilmesi yasal suç teşkil eder.</li>
            <li>Yazılım isminin değiştirilerek "kendi projem" şeklinde sunulması fikri mülkiyet hırsızlığıdır.</li>
        </ul>

        <h3>3. Teknik Çekirdek Bilgisi</h3>
        <p>Sistem, Yusuf Tatlıcak tarafından optimize edilen <b>KUTAY 1.5 FLASH</b> motoru üzerinden çalışmaktadır.</p>
        
        <p style="background-color: #F1F8FF; padding: 25px; border-radius: 12px; color: #1E429F; font-weight: bold; text-align: center; border: 2px solid #C3DDFD; margin-top: 30px;">
            ⚖️ 2026 Yusuf Tatlıcak Cyber Security Lab - Her Hakkı Saklıdır.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif nav == "📜 Arşiv":
    st.title("📜 Konuşma Arşivi")
    if not st.session_state.messages:
        st.info("Sistem belleği şu an boş.")
    else:
        for m in st.session_state.messages:
            lbl = "Yusuf" if m["role"] == "user" else "KUTAY AI"
            st.text_area(f"Kaynak: {lbl}", value=m["content"], height=100, disabled=True)
