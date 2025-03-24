import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import speech_recognition as sr
import pyttsx3
from ai import chat_with_ai, execute_command  # Import AI functions

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

# Get available voices
voices = engine.getProperty('voices')
voice_options = {
    "Male": voices[0].id,
    "Female": voices[1].id if len(voices) > 1 else voices[0].id
}

class AIAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Assistant")
        self.root.attributes('-fullscreen', True)  # Open in fullscreen
        self.root.configure(bg="#1E1E1E")  # Dark theme

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#252526", fg="#00AEEF", font=("San Francisco", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.insert(tk.END, "Connect AI: Here, Lord Amara!\n")
        self.chat_display.config(state=tk.DISABLED)

        # Voice selection
        self.voice_label = tk.Label(root, text="Voice:", font=("Arial", 12), bg="#1E1E1E", fg="white")
        self.voice_label.pack(pady=5)

        self.voice_var = tk.StringVar(value="Male")
        self.voice_dropdown = ttk.Combobox(root, textvariable=self.voice_var, values=list(voice_options.keys()), state="readonly")
        self.voice_dropdown.pack(pady=5)

        # Status label
        self.status_label = tk.Label(root, text="Listening...", font=("Arial", 12), bg="#1E1E1E", fg="#00AEEF")
        self.status_label.pack(pady=5)

        self.listening = True  # Flag to control listening

        # Start listening immediately when the GUI opens
        self.start_listening()

        # Press `Esc` to exit fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)

    def update_chat(self, text):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def speak(self, text):
        """Speaks the given text aloud using the selected voice."""
        selected_voice = voice_options[self.voice_var.get()]
        engine.setProperty('voice', selected_voice)
        engine.say(text)
        engine.runAndWait()

    def listen_for_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.status_label.config(text="I'm Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                self.update_chat("You: " + command)

                if "exit" in command:  # Stop listening and close app
                    self.update_chat("Connect AI: Bye!")
                    self.listening = False
                    self.root.quit()  # Close the GUI
                    return
                
                self.process_command(command)

            except sr.UnknownValueError:
                self.update_chat("Connect AI: Speak clearly.")
            except sr.RequestError:
                self.update_chat("Connect AI: Must be MTN.")
            except sr.WaitTimeoutError:
                self.update_chat("Connect AI: Didn't hear anything.")

        self.status_label.config(text="Listening...")  # Reset status
        if self.listening:
            self.start_listening()  # Keep listening unless stopped

    def process_command(self, command):
        response = execute_command(command)  # Try to execute a command
        if "Error:" in response or "not found" in response.lower():  
            response = chat_with_ai(command)  # If no command matches, chat with AI
        self.update_chat("AI: " + response)
        self.speak(response)  # Speak out the response

    def start_listening(self):
        if self.listening:
            threading.Thread(target=self.listen_for_command, daemon=True).start()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)  # Exit fullscreen

if __name__ == "__main__":
    root = tk.Tk()
    gui = AIAssistantGUI(root)
    root.mainloop()
