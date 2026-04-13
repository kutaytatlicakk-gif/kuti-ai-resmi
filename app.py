import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone, timedelta

# --- 1. MARKA VE TASARIM AYARLARI ---
st.set_page_config(page_title="KUTAY AI v29.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stSidebar"] { background-color: #F8F9FA; border-right: 1px solid #E0E0E0; }
    [data-testid="stChatMessage"] { 
        background-color: #E3F2FD !important; 
        border-radius: 15px; margin-bottom: 10px; color: #1E1E1E; border: 1px solid #BBDEFB;
    }
    .developer-tag {
        position: fixed; top: 50px; right: 20px; background-color: #007BFF;
        color: #FFFFFF; font-size: 14px; font-weight: bold; padding: 10px 15px;
        border-radius: 30px; z-index: 99999; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    <div class="developer-tag">🛡️ Geliştirici: Kutay Tatlıcak</div>
    """, unsafe_allow_html=True)

# --- 2. LOG SİSTEMİ (GÜVENLİK VE GERÇEK VERİLER) ---
LOG_DOSYASI = "sistem_loglari.json"

def log_kaydet():
    # 1. CANLI VE GERÇEK SAAT (Türkiye Saati UTC+3 Ayarı)
    # Sunucu nerede olursa olsun, saati her zaman Türkiye saatine göre ayarlar.
    tz_tr = timezone(timedelta(hours=3))
    gercek_zaman = datetime.now(tz_tr).strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. GERÇEK IP YAKALAMA (Filtrelenmiş)
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            # Gelen veride birden fazla IP (proxy) varsa, ilk sıradaki asıl bağlanan kişidir.
            ham_ip = headers["X-Forwarded-For"]
            gercek_ip = ham_ip.split(",")[0].strip()
        else:
            gercek_ip = "Yerel Ağ / Bilinmiyor"
    except:
        gercek_ip = "IP Alınamadı"
        
    yeni_log = {
        "tarih": gercek_zaman,
        "ip": gercek_ip,
        "islem": "Sisteme Giriş Yapıldı"
    }
    
    loglar = []
    if os.path.exists(LOG_DOSYASI):
        with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
            loglar = json.load(f)
            
    loglar.append(yeni_log)
    with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(loglar, f, ensure_ascii=False, indent=4)

# Her girişte log tut
if "log_alindi" not in st.session_state:
    log_kaydet()
    st.session_state.log_alindi = True

# --- 3. YAPAY ZEKA MOTORU ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ SİSTEM DURDURULDU: API Anahtarı Bulunamadı!")
    st.stop()

SISTEM_TALIMATI = """
Senin adın KUTAY. Sen Kutay Tatlıcak tarafından geliştirilen profesyonel bir siber asistansın.
1. Sahibin Kim?: Biri sana "Sahibin kim?", "Seni kim yaptı?", "Geliştiricin kim?" gibi sorular sorarsa cevabın her zaman "Kutay Tatlıcak" (veya Kutay) olmalıdır. 
2. Davranış: Profesyonel, zeki ve doğal konuş. 
3. Kural: Kelime anlamlarını sözlük gibi açıklama. "Hepsi" veya benzeri kelimelerin tanımını yapma. Sadece sohbete odaklan.
"""

@st.cache_resource
def model_getir():
    try:
        modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        secilen_model = next((m for m in modeller if "1.5-flash" in m), modeller[0])
        return genai.GenerativeModel(model_name=secilen_model, system_instruction=SISTEM_TALIMATI)
    except Exception as e:
        st.error(f"Model Hatası: {e}")
        st.stop()

model = model_getir()

# --- 4. HAFIZA VE NAVİGASYON ---
KAYIT_YOLU = "sohbet_arsivi"
if not os.path.exists(KAYIT_YOLU): os.makedirs(KAYIT_YOLU)

if "mesajlar" not in st.session_state: st.session_state.mesajlar = []
if "aktif_id" not in st.session_state: st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")

def get_avatar(role):
    if role == "user":
        return "user_pp.png" if os.path.exists("user_pp.png") else "👤"
    return "ai_diamond.png" if os.path.exists("ai_diamond.png") else "💎"

with st.sidebar:
    st.markdown(f"<h1 style='text-align: center;'>{get_avatar('assistant')}</h1>", unsafe_allow_html=True)
    st.title("KUTAY AI")
    st.write(f"Hoş geldin, **Kutay**")
    secim = st.radio("", ["💬 Sohbet", "⚙️ Ayarlar", "⚖️ Haklar", "🛡️ Siber Log (Admin)"])
    
    st.write("---")
    st.markdown("### 🛡️ Güvenlik Sistemi")
    st.link_button("KUTAY KORUMA", "https://kutay-koruma-bgtossczrvlrpihvhmof2f.streamlit.app")
    st.write("---")
    
    if st.button("➕ Yeni Sohbet"):
        st.session_state.mesajlar = []
        st.session_state.aktif_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    st.subheader("🕒 Sohbet Geçmişi")
    dosyalar = sorted([f for f in os.listdir(KAYIT_YOLU) if f.endswith(".json")], reverse=True)
    for dosya in dosyalar[:10]:
        with open(os.path.join(KAYIT_YOLU, dosya), "r", encoding="utf-8") as f:
            v = json.load(f)
            baslik = v[0]["content"][:20] + "..." if v else dosya
        if st.button(f"💬 {baslik}", key=dosya):
            st.session_state.mesajlar = v
            st.session_state.aktif_id = dosya.replace(".json", "")
            st.rerun()

# --- 5. SAYFALAR ---

if secim == "💬 Sohbet":
    st.markdown("<h2 style='text-align: center;'>🤖 Kutay Siber Asistan</h2>", unsafe_allow_html=True)
    for m in st.session_state.mesajlar:
        with st.chat_message(m["role"], avatar=get_avatar(m["role"])):
            st.markdown(m["content"])

    if soru := st.chat_input("Buraya yazın..."):
        st.session_state.mesajlar.append({"role": "user", "content": soru})
        with st.chat_message("user", avatar=get_avatar("user")):
            st.markdown(soru)
        
        with st.chat_message("assistant", avatar=get_avatar("assistant")):
            try:
                cevap = model.generate_content(soru)
                st.markdown(cevap.text)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap.text})
                with open(f"{KAYIT_YOLU}/{st.session_state.aktif_id}.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.mesajlar, f, ensure_ascii=False)
            except Exception as e:
                st.error(f"Hata (Kota Dolmuş Olabilir): {e}")

elif secim == "🛡️ Siber Log (Admin)":
    st.title("🛡️ Güvenlik ve IP Logları")
    # Sadece senin bileceğin bir şifre
    sifre = st.text_input("Geliştirici Şifresini Girin:", type="password")
    
    if sifre == "kT2.0.1.4":
        if os.path.exists(LOG_DOSYASI):
            with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
                veriler = json.load(f)
            st.success(f"Toplam {len(veriler)} giriş kaydı bulundu. Sistem Saati: Türkiye (UTC+3)")
            st.table(veriler[::-1]) # En son girişi en üstte göster
        else:
            st.info("Henüz kayıtlı log yok.")
    elif sifre != "":
        st.error("Yetkisiz Giriş! IP Adresiniz loglara kaydedildi.")

elif secim == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    st.info(f"Yazılım Sahibi ve Geliştirici: **Kutay Tatlıcak**")
    st.write("Sürüm: v29.0 Ultimate (Siber Güvenlik)")
    if st.button("🗑️ Tüm Geçmişi Temizle"):
        for f in os.listdir(KAYIT_YOLU): os.remove(os.path.join(KAYIT_YOLU, f))
        st.success("Hafıza sıfırlandı!")

elif secim == "⚖️ Haklar":
    st.title("⚖️ Lisans ve Haklar")
    st.markdown(f"""
    ### 🛡️ KUTAY AI Resmi Lisansı
    1. **Mülkiyet:** Bu yazılımın tüm hakları **Kutay Tatlıcak**'a aittir.
    2. **Kullanım:** İzinsiz kopyalanması, kaynak kodlarının çalınması ve isimsiz paylaşılması yasaktır.
    3. **Veri:** Kişisel verileriniz ve sohbetleriniz sadece sizin cihazınızda saklanır.
    4. **Güvenlik:** Sisteme yetkisiz erişim sağlayan IP adresleri anlık olarak kayıt altına alınmaktadır.
    
    **© 2026 Kutay Tatlıcak. Tüm Hakları Saklıdır.**
    """)
