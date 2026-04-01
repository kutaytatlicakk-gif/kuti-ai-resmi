import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KutiAİ Özel", page_icon="🔐")

# --- ŞİFRE KONTROLÜ ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["ACCESS_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 KutiAİ Giriş")
        st.text_input("Giriş Şifresi:", type="password", on_change=password_entered, key="password")
        return False
    return True

if check_password():
    st.title("🤖 KutiAİ v13.0")
    
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # En güncel ve hatasız model çağırma yöntemi
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Secrets kısmına API anahtarını ekle!")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Mesajını yaz..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            try:
                # Karmaşık ayarları çıkardık, direkt yanıt alıyoruz
                response = model.generate_content(p)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Hata: {str(e)}")
