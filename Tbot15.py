import sys

# ============================================================
#   FIX IMPORT TKINTER (Python 3.14 compatibilità)
# ============================================================

try:
    import tkinter as tk
    from tkinter import scrolledtext
except Exception as e:
    print("❌ ERRORE: Tkinter non è installato correttamente.")
    print("➡ Soluzione: reinstalla Python da python.org e attiva 'tcl/tk and IDLE'.")
    print("Dettagli errore:", e)
    sys.exit(1)

# ============================================================
#   IMPORT AUDIO (senza PyAudio)
# ============================================================

try:
    import sounddevice as sd
    import soundfile as sf
    import speech_recognition as sr
    import numpy as np
except Exception as e:
    print("❌ ERRORE: Moduli audio mancanti.")
    print("Installa con:")
    print("pip install sounddevice soundfile SpeechRecognition numpy")
    print("Dettagli errore:", e)
    sys.exit(1)

import time
import threading
import datetime
import tempfile
import os

recognizer = sr.Recognizer()

# ============================================================
#   FUNZIONE REGISTRAZIONE AUDIO (compatibile 3.14)
# ============================================================

def record_audio(duration=5, samplerate=44100):
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate,
                       channels=1, dtype='float32')
        sd.wait()
        return audio, samplerate
    except Exception as e:
        print("Errore registrazione audio:", e)
        return None, None

def recognize_speech():
    audio, samplerate = record_audio()

    if audio is None:
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        sf.write(tmp.name, audio, samplerate)
        temp_path = tmp.name

    try:
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="it-IT")
    except:
        text = None

    os.remove(temp_path)
    return text

# ============================================================
#   LOGICA TBOT15
# ============================================================

def tbot15_response(msg):
    msg = msg.lower().strip()

    if msg == "":
        return "Dimmi pure qualcosa, sono qui."

    if "ciao" in msg:
        return "Ciao! Sono TBOT15, assistente Windows 11."

    if "chi sei" in msg:
        return "Sono TBOT15, stile Cortana, compatibile con Windows 11 23H2/24H2."

    if "come stai" in msg:
        return "Sto bene! Pronto ad aiutarti."

    if "windows 11" in msg:
        return "Windows 11 23H2/24H2 porta nuove funzioni AI e stabilità."

    if "wifi" in msg:
        return "Per il Wi‑Fi: clicca in basso a destra → icona rete → scegli la rete."

    if "volume" in msg:
        return "Per il volume: clicca sull’icona dell’altoparlante in basso a destra."

    if "equazione" in msg:
        return "Un’equazione di primo grado ha forma ax + b = c. Vuoi un esempio?"

    if "cellula" in msg:
        return "La cellula è l’unità base della vita. Esistono cellule animali e vegetali."

    return "Interessante! Vuoi chiedermi qualcosa su Windows 11 o su una materia scolastica?"

# ============================================================
#   GUI TBOT15 (FIXATA)
# ============================================================

class TBOT15GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TBOT15 – Assistente Windows 11")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f0f0f")

        # Chat
        self.chat = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="#0f0f0f", fg="#ffffff",
            font=("Segoe UI", 11), state="disabled"
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input
        self.entry = tk.Entry(root, bg="#2a2a2a", fg="#ffffff",
                              font=("Segoe UI", 11), relief=tk.FLAT)
        self.entry.pack(fill=tk.X, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)

        # Microfono
        self.mic_btn = tk.Button(root, text="🎤", bg="#4ea3ff",
                                 fg="#000000", font=("Segoe UI", 12, "bold"),
                                 command=self.start_voice)
        self.mic_btn.pack(pady=5)

        self.add_bot("Ciao! Sono TBOT15. Scrivi o parla con il microfono.")

    def add_user(self, text):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"\n🧑 Tu:\n{text}\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def add_bot(self, text):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"\n🤖 TBOT15:\n{text}\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if text == "":
            return
        self.entry.delete(0, tk.END)
        self.add_user(text)
        self.add_bot(tbot15_response(text))

    def start_voice(self):
        threading.Thread(target=self.voice_worker, daemon=True).start()

    def voice_worker(self):
        self.add_bot("Sto ascoltando…")
        text = recognize_speech()
        if not text:
            self.add_bot("Non ho capito, puoi ripetere?")
            return
        self.add_user(text)
        self.add_bot(tbot15_response(text))

# ============================================================
#   AVVIO SICURO
# ============================================================

try:
    root = tk.Tk()
    TBOT15GUI(root)
    root.mainloop()
except Exception as e:
    print("❌ ERRORE: impossibile avviare la GUI Tkinter.")
    print("➡ Tkinter potrebbe non essere installato correttamente in Python 3.14.")
    print("Dettagli:", e)
