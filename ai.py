import google.generativeai as genai
import pyautogui
import os
import keyboard
import webbrowser

#  Gemini API
GEMINI_API_KEY = "AIzaSyCpIfUjFvJgJjz_PtTrpyF7ppEA60HU32Q"
genai.configure(api_key=GEMINI_API_KEY)

# Amara is a beast 
model = genai.GenerativeModel("gemini-1.5-pro-latest")

#idk what to comment 
custom_apps = {
    "spotify": r"C:\Users\Amara\AppData\Roaming\Spotify\Spotify.exe",
    "vs code": r"C:\Users\Amara\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}

#im tired of gemini
#why tf is this api key not working 
#oh ive found it. my key didnt have the right gemini model on it 😭
def chat_with_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# now gemini is answering my predefined commands like its a question. what did i do to deserve this?
#maybe i'll return the execute command() first then the achat_with_ai(prompt) later
#it didnt work😞
#ohhhhh shit i returned the chat_with_ai in the gui.py. na me dey always do myself tbh😭😭😭
def execute_command(command):
    command = command.lower()
    
    print(f"Noted boss: {command}")

    # Open System Applications
    system_apps = {
        "open browser": "start chrome",
        "open notepad": "notepad",
        "open file explorer": "explorer",
        "open calculator": "calc",
    }

    for key, value in system_apps.items():
        if key in command:
            os.system(value)
            return f"{key.capitalize()}..."

    # Open apps that are not system based 
    for app in custom_apps:
        if f"open {app}" in command:
            try:
                os.startfile(custom_apps[app])
                return f"Opening {app}..."
            except FileNotFoundError:
                return f"Error: {app} not found."

    # control my volume
    volume_controls = {
        "increase volume": "volume up",
        "decrease volume": "volume down",
        "mute volume": "volume mute",
        "unmute volume": "volume mute",
    }

    for key, value in volume_controls.items():
        if key in command:
            for _ in range(5):
                keyboard.press_and_release(value)
            return key.capitalize()

    # pause and play the musoc 
    media_controls = {
        "play music": "play/pause media",
        "pause music": "play/pause media",
        "next track": "next track",
        "previous track": "previous track",
    }

    for key, value in media_controls.items():
        if key in command:
            keyboard.press_and_release(value)
            return key.capitalize()

    # take Screenshots
    if "take screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot taken and saved."

    # close windows 
    if "close window" in command:
        pyautogui.hotkey("alt", "f4")
        return "Closing window..."
    
    if "lock screen" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking screen..."

    # Shutdown nd Restart
    shutdown_commands = {
        "shutdown my pc": "shutdown /s /t 10",
        "restart my pc": "shutdown /r /t 10",
        "cancel shutdown": "shutdown /a",
    }

    for key, value in shutdown_commands.items():
        if key in command:
            os.system(value)
            return key.capitalize()

    # might add my crypto websites
    websites = {
        "open youtube": "https://www.youtube.com",
        "open google": "https://www.google.com",
        "open facebook": "https://www.facebook.com",
        "open github": "https://www.github.com",
        "open crypto": "https://dashboard.layeredge.io/",
        "i want to watch anime": "https://9animetv.to/home",
        "open school":"w3schools.com"
    }

    for key, value in websites.items():
        if key in command:
            webbrowser.open(value)
            return f"Opening {key.split()[-1].capitalize()}..."

    # if it dosent find a predefined command it should treat what i said as a question and contact gemini api
    return chat_with_ai(command)

# Test 
if __name__ == "__main__":
    while True:
        command = input("Enter command: ")
        if command.lower() == "exit":
            break
        print(execute_command(command))


