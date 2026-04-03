import customtkinter as ctk
import google.generativeai as genai
import json
import os
import threading
from datetime import datetime

# --- GEMINI YAPILANDIRMASI ---
# Buraya kendi API anahtarını yapıştırmayı unutma!
API_KEY = "AIzaSyDJBlDIHija8IxAPL8AuQkn-4NahQZs1qE"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- GÖRSEL AYARLAR ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class KutiAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KUTI-AI v15.0 | SİBER ASİSTAN")
        self.geometry("1000x650")

        # Geçmişi yükle
        self.history_file = "kuti_history.json"
        self.messages = self.load_history()

        # --- SOL PANEL (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.logo = ctk.CTkLabel(self.sidebar, text="⚡ KUTI-AI PRO", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=20)

        # Sistem Durum Paneli
        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="#1a1a1a")
        self.status_frame.pack(fill="x", padx=10, pady=10)
        self.status_label = ctk.CTkLabel(self.status_frame, text="SİSTEM: AKTİF\nAPI: BAĞLI", font=("Fixedsys", 12), text_color="#00FF00")
        self.status_label.pack(pady=10)

        # Geçmiş Listesi
        self.history_label = ctk.CTkLabel(self.sidebar, text="Sohbet Kayıtları", font=("Fixedsys", 14))
        self.history_label.pack(pady=(20, 5))
        
        self.history_display = ctk.CTkTextbox(self.sidebar, width=200, height=300, font=("Segoe UI", 11))
        self.history_display.pack(pady=10, padx=10)
        self.update_history_display()

        # Temizleme Butonu
        self.clear_btn = ctk.CTkButton(self.sidebar, text="GEÇMİŞİ SIFIRLA", fg_color="#8B0000", hover_color="#FF0000", command=self.clear_history)
        self.clear_btn.pack(side="bottom", pady=20)

        # --- ANA SOHBET ALANI ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.chat_box = ctk.CTkTextbox(self.main_frame, font=("Segoe UI", 14))
        self.chat_box.pack(pady=10, padx=10, fill="both", expand=True)
        self.chat_box.insert("end", "KutiAI: Merhaba Yusuf! Bugün hangi projeyi geliştiriyoruz?\n\n")

        # Giriş Alanı ve Buton
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill="x", side="bottom", pady=10)

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Mesajınızı yazın...", height=40)
        self.user_input.pack(side="left", fill="x", expand=True, padx=(10, 5))
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="GÖNDER", width=100, height=40, command=self.send_message)
        self.send_btn.pack(side="right", padx=(5, 10))

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self, role, text):
        self.messages.append({"role": role, "text": text, "time": datetime.now().strftime("%H:%M")})
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)
        self.update_history_display()

    def update_history_display(self):
        self.history_display.configure(state="normal")
        self.history_display.delete("1.0", "end")
        for msg in self.messages[-10:]: # Son 10 mesajın özetini göster
            prefix = "Siz: " if msg["role"] == "user" else "AI: "
            self.history_display.insert("end", f"{prefix}{msg['text'][:20]}...\n")
        self.history_display.configure(state="disabled")

    def clear_history(self):
        self.messages = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        self.chat_box.delete("1.0", "end")
        self.history_display.configure(state="normal")
        self.history_display.delete("1.0", "end")
        self.history_display.configure(state="disabled")
        self.chat_box.insert("end", "Sistem sıfırlandı. Yeni oturum başladı.\n\n")

    def send_message(self):
        user_text = self.user_input.get()
        if not user_text.strip(): return

        self.chat_box.insert("end", f"Yusuf: {user_text}\n")
        self.user_input.delete(0, "end")
        self.save_history("user", user_text)

        # Gemini cevabını arka planda al (Donma yapmaması için)
        threading.Thread(target=self.get_ai_response, args=(user_text,), daemon=True).start()

    def get_ai_response(self, prompt):
        try:
            response = model.generate_content(prompt)
            ai_text = response.text
            self.chat_box.insert("end", f"KutiAI: {ai_text}\n\n")
            self.chat_box.see("end")
            self.save_history("bot", ai_text)
        except Exception as e:
            self.chat_box.insert("end", f"SİSTEM HATASI: {str(e)}\n\n")

if __name__ == "__main__":
    app = KutiAI()
    app.mainloop()
