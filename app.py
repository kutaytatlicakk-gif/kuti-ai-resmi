import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="KutiAİ Özel", page_icon="🔐", layout="centered")

# --- ŞİFRE KONTROLÜ ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["ACCESS_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 KutiAİ Sistem Girişi")
        st.text_input("Giriş Şifresi:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Hatalı Şifre! Tekrar Dene:", type="password", on_change=password_entered, key="password")
        st.error("Erişim Reddedildi.")
        return False
    else:
        return True

# Şifre doğruysa asistanı aç
if check_password():
    st.title("🤖 KutiAİ v13.0")
    st.caption("Sadece Yusuf Tatlıcak'a özel güvenli bağlantı.")

    # API Yapılandırması
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 404 hatasını aşmak için v1 zorlaması
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        request_options = RequestOptions(api_version="v1")
    else:
        st.error("Secrets kısmına API anahtarını ekle!")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Mesajını buraya bırak..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            try:
                # request_options=request_options kısmı 404'ü engeller
                response = model.generate_content(p, request_options=request_options)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem Hatası: {str(e)}")
