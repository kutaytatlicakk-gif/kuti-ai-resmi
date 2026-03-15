import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KutiAİ v12", page_icon="🤖")
st.title("🤖 KutiAİ v12 - Online")

# API Anahtarı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # 404 hatasını önlemek için v1beta yerine ana yolu kullanan model
    model = genai.GenerativeModel('gemini-1.5-flash')
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
            # ÖNEMLİ: Bazı eski kütüphane hatalarını aşmak için stream kullanıyoruz
            response = model.generate_content(p)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sistem Hatası: {str(e)}")
