import os
import threading
import tkinter as tk
import speech_recognition as sr
from PIL import Image, ImageTk

class WakeWordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("connect launcher")
        self.root.geometry("300x300")
        self.root.configure(bg="#1E1E1E")

        # Load microphone image
        self.mic_image = Image.open("mic_off.png")  # Default icon
        self.mic_image = self.mic_image.resize((100, 100), Image.LANCZOS)
        self.mic_photo = ImageTk.PhotoImage(self.mic_image)

        self.mic_label = tk.Label(root, image=self.mic_photo, bg="#1E1E1E")
        self.mic_label.pack(expand=True)

        self.listening = True
        self.recognizer = sr.Recognizer()

        # Start listening in a thread
        threading.Thread(target=self.listen_for_wake_word, daemon=True).start()

    def listen_for_wake_word(self):
        wake_word = "i connect"  
        wake_word = "iconnect"
        wake_word = "hi connect"

        with sr.Microphone() as source:
            print("Listening for masters command...")

            while self.listening:
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    detected_text = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: {detected_text}")

                    if wake_word in detected_text:
                        print("calling connect🏃‍♂️‍➡️...")
                        self.update_mic_icon("mic_on.png")  # Change mic icon
                        os.system("python gui.py")  # Launch AI GUI
                        self.listening = False
                        break  

                except sr.UnknownValueError:
                    pass  
                except sr.RequestError:
                    print("Error: something is wrong .")
                    break

            self.update_mic_icon("mic_off.png")  # Reset mic icon

    def update_mic_icon(self, icon_path):
        self.mic_image = Image.open(icon_path)
        self.mic_image = self.mic_image.resize((100, 100), Image.LANCZOS)
        self.mic_photo = ImageTk.PhotoImage(self.mic_image)
        self.mic_label.config(image=self.mic_photo)

if __name__ == "__main__":
    root = tk.Tk()
    app = WakeWordGUI(root)
    root.mainloop()
