import customtkinter as ctk
import google.generativeai as genai
import json
import os
import threading
from datetime import datetime

# --- YENİ API ANAHTARI ENTEGRASYONU ---
API_KEY = "AIzaSyAy4UAzQafV4GmwdNo_w6tS3dmzirD0P4Q"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- GÖRSEL TEMA ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class KutiAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KUTI-AI v15.0 | SİBER HAFIZA SİSTEMİ")
        self.geometry("1000x650")

        # Geçmiş Dosyası Kontrolü
        self.history_file = "kuti_data.json"
        self.history_data = self.load_history()

        # --- SIDEBAR (SOL PANEL) ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.logo = ctk.CTkLabel(self.sidebar, text="KUTI-AI PRO", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=20)

        # Durum Göstergesi
        self.status_box = ctk.CTkFrame(self.sidebar, fg_color="#0f0f0f", height=60)
        self.status_box.pack(fill="x", padx=15, pady=10)
        self.status_text = ctk.CTkLabel(self.status_box, text="● SİSTEM: ÇEVRİMİÇİ\n● MOD: HAFIZA AKTİF", 
                                        font=("Fixedsys", 11), text_color="#00FF00")
        self.status_text.pack(pady=10)

        # Geçmiş Listesi
        ctk.CTkLabel(self.sidebar, text="Sohbet Geçmişi", font=("Fixedsys", 14)).pack(pady=(15, 5))
        self.history_list = ctk.CTkTextbox(self.sidebar, width=210, height=320, font=("Segoe UI", 11), fg_color="#1a1a1a")
        self.history_list.pack(pady=5, padx=10)
        self.refresh_history_view()

        # Temizle Butonu
        self.clear_btn = ctk.CTkButton(self.sidebar, text="HAFIZAYI SİL", fg_color="#660000", 
                                        hover_color="#AA0000", command=self.clear_all_data)
        self.clear_btn.pack(side="bottom", pady=20)

        # --- ANA EKRAN ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.chat_screen = ctk.CTkTextbox(self.main_area, font=("Segoe UI", 14), spacing2=5)
        self.chat_screen.pack(pady=10, padx=10, fill="both", expand=True)
        self.chat_screen.insert("end", "KutiAI: Sistem başlatıldı. Merhaba Yusuf, seni dinliyorum...\n\n")

        # Giriş Çubuğu
        self.bottom_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.bottom_bar.pack(fill="x", side="bottom", pady=10)

        self.entry = ctk.CTkEntry(self.bottom_bar, placeholder_text="Siber komut veya mesaj girin...", height=45)
        self.entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        self.entry.bind("<Return>", lambda e: self.process_chat())

        self.btn = ctk.CTkButton(self.bottom_bar, text="GÖNDER", width=110, height=45, command=self.process_chat)
        self.btn.pack(side="right", padx=(5, 10))

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_to_history(self, user_msg, ai_msg):
        entry = {
            "time": datetime.now().strftime("%H:%M"),
            "user": user_msg[:30] + "...",
            "full_user": user_msg,
            "full_ai": ai_msg
        }
        self.history_data.append(entry)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, ensure_ascii=False, indent=4)
        self.refresh_history_view()

    def refresh_history_view(self):
        self.history_list.configure(state="normal")
        self.history_list.delete("1.0", "end")
        for item in reversed(self.history_data[-15:]): # Son 15 kaydı göster
            self.history_list.insert("end", f"[{item['time']}] {item['user']}\n---\n")
        self.history_list.configure(state="disabled")

    def clear_all_data(self):
        self.history_data = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        self.chat_screen.delete("1.0", "end")
        self.chat_screen.insert("end", ">> SİSTEM TEMİZLENDİ. YENİ OTURUM.\n\n")
        self.refresh_history_view()

    def process_chat(self):
        msg = self.entry.get()
        if not msg.strip(): return
        
        self.chat_screen.insert("end", f"Yusuf: {msg}\n")
        self.entry.delete(0, "end")
        
        threading.Thread(target=self.call_gemini, args=(msg,), daemon=True).start()

    def call_gemini(self, prompt):
        try:
            response = model.generate_content(prompt)
            answer = response.text
            self.chat_screen.insert("end", f"KutiAI: {answer}\n\n")
            self.chat_screen.see("end")
            self.save_to_history(prompt, answer)
        except Exception as e:
            self.chat_screen.insert("end", f"HATA: Bağlantı kurulamadı. {e}\n\n")

if __name__ == "__main__":
    app = KutiAI()
    app.mainloop()
