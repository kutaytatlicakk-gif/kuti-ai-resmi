import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="KutiAİ v12", page_icon="🤖")
st.title("🤖 KutiAİ v12 - Online")

if "GOOGLE_API_KEY" in st.secrets:
    # API anahtarını yapılandır
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # İŞTE KRİTİK NOKTA: v1beta hatasından kaçmak için zorunlu ayar
    # Bu ayar Google'a "beta versiyonu değil, kararlı versiyonu kullan" der.
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"speed_optimized": True}
    )
    # Bağlantı ayarlarını v1 olarak zorluyoruz
    request_options = RequestOptions(api_version="v1")
else:
    st.error("Secrets kısmına API anahtarını ekle!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Naber kanka?"):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        try:
            # Buradaki request_options o 404 hatasını bypass eder
            response = model.generate_content(p, request_options=request_options)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sistem Hatası: {str(e)}")
