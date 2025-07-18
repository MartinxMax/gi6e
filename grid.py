from lib.GI6E import *
import questionary
import time
import random
import string
import os

AUTH = 'Maptnh@S-H4CK13'
NAME = 'GI6E'
WEB = 'https://github.com/MartinxMax'
VERSION = '1.2'
PROMPT = 'Who U R ?'

LOGO = f'''
         |G R I D|
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡀⠀⠀⢀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣤⣤⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⣠⠀⣶⣤⣄⣉⣉⣉⣉⣠⣤⣶⠀⣄⣀⡀⠀⠀⠀⠀⠀⠀ {'_'*len(PROMPT)}
⠀⠀⠀⣶⣾⣿⣿⣿⣿⣦⣄⣉⣙⣛⣛⣛⣛⣋⣉⣠⣴⣿⣿⣿⣿⣷⣶⠀⠀< {PROMPT}|
⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠛⠛⠉⠉⠁⠀⠀⠀⠀ {'`'*len(PROMPT)}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⣆⠀⠀⠀⢠⡄⠀⠀⠀⣰⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⣶⣾⣿⡆⠸⣿⣶⣶⣾⣿⣿⣷⣶⣶⣿⠇⢰⣿⣷⣶⣄⡀⠀⠀⠀     {AUTH}
⠀⠀⠺⠿⣿⣿⣿⣿⣿⣄⠙⢿⣿⣿⣿⣿⣿⣿⡿⠋⣠⣿⣿⣿⣿⣿⠿⠗⠀⠀{NAME}-{VERSION}
⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣷⡄⠈⠙⠛⠛⠋⠁⢠⣾⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣀⣤⣬⣿⣿⣿⣇⠐⣿⣿⣿⣿⠂⣸⣿⣿⣿⣥⣤⣀⠀⠀⠀{WEB}
⠀⠀⠀⠀⠘⠻⠿⠿⢿⣿⣿⣿⣧⠈⠿⠿⠁⣼⣿⣿⣿⡿⠿⠿⠟⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⠀⣶⣦⠀⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

def random_key(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def input_text():
    return questionary.text("Please enter text to convert:").ask()

def input_grid_code():
    return questionary.text("Please enter Grid code (space separated):").ask()

def get_key():
    mode = questionary.select(
        "Select key mode:",
        choices=[
            "1. Auto generate random key",
            "2. Manually enter key (8+ chars)"
        ]).ask()
    if mode.startswith("1"):
        key = random_key(8)
        print(f"Random key generated: {key}")
        return key
    while True:
        key = questionary.text("Please enter key (8+ chars):").ask()
        if key and len(key) >= 8:
            return key
        print("Key length insufficient, please re-enter.")

def gen_wav(text, key=None):
    g = grid()
    data, path = g.text_2_grid(text=text, wav=True, key=key)
    mode = "[Encrypted]" if key else "[Unencrypted]"
    if not data:
        print(f"{mode} Failed to generate WAV: Invalid key format.")
        return None
    print(f"{mode} WAV generated: {path}")
    return path

def decode_wav(path, key=None):
    g = grid()
    mode = "[Encrypted]" if key else "[Unencrypted]"
    result = g.wav_2_text(wav_path=path, key=key)
    if not result:
        print(f"{mode} Decoding failed.")
        return None
    print(f"{mode} Decoded result => {result}")
    return result

def text_to_grid(text, key=None):
    g = grid()
    data = g.text_2_grid(text=text, wav=False, key=key)[0]
    mode = "[Encrypted]" if key else "[Unencrypted]"
    print(f"{mode} Generated Grid code => '{data}'")
    return data

def main():
    g = grid()
    print("=== GI6E Morse Grid Communication System ===")
    while True:
        choice = questionary.select(
            "Select function:",
            choices=[
                "1. Text to WAV (Unencrypted)",
                "2. Text to WAV (Encrypted)",
                "3. WAV to Text (Unencrypted)",
                "4. WAV to Text (Encrypted)",
                "5. One-click test",
                "6. Real-time listen (Unencrypted)",
                "7. Real-time listen (Encrypted)",
                "8. Text to Grid (Unencrypted)",
                "9. Text to Grid (Encrypted)",
                "10. Grid to Text (Unencrypted)",
                "11. Grid to Text (Encrypted)",
                "0. Exit"
            ]).ask()

        if choice.startswith("1."):
            txt = input_text()
            if txt: gen_wav(txt)

        elif choice.startswith("2."):
            txt = input_text()
            if txt:
                k = get_key()
                gen_wav(txt, key=k)

        elif choice.startswith("3."):
            p = questionary.path("Enter unencrypted WAV path:").ask()
            if p and os.path.isfile(p): decode_wav(p)

        elif choice.startswith("4."):
            p = questionary.path("Enter encrypted WAV path:").ask()
            if p and os.path.isfile(p):
                k = get_key()
                decode_wav(p, key=k)

        elif choice.startswith("5."):
            print("=== One-click test start ===")
            test_text = "TEST" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            test_key = random_key(8)
            print(f"Test text: {test_text}, Test key: {test_key}")
            path = gen_wav(test_text, key=test_key)
            if not path:
                print("WAV generation failed, stopping test.")
                continue
            time.sleep(1)
            decode_wav(path, key=test_key)

        elif choice.startswith("6."):
            print("Audio device list =>", g.get_audio_list())
            print("Start real-time listening, please play signal and keep environment quiet...")
            result = g.realtime_grid_detection()
            print("[Real-time listen][Unencrypted] Decoded result =>", result)

        elif choice.startswith("7."):
            k = get_key()
            print("Audio device list =>", g.get_audio_list())
            print("Start real-time listening, please play signal and keep environment quiet...")
            result = g.realtime_grid_detection(key=k)
            print("[Real-time listen][Encrypted] Decoded result =>", result)

        elif choice.startswith("8."):
            txt = input_text()
            if txt: text_to_grid(txt)

        elif choice.startswith("9."):
            txt = input_text()
            if txt:
                k = get_key()
                text_to_grid(txt, key=k)

        elif choice.startswith("10."):
            code = input_grid_code()
            if code:
                res = g.grid_2_text(code)
                print("[Unencrypted] Decoded:", res)

        elif choice.startswith("11."):
            code = input_grid_code()
            if code:
                k = get_key()
                res = g.grid_2_text(code, key=k)
                print("[Encrypted] Decoded:", res)

        elif choice.startswith("0."):
            print("Exiting program.")
            break

        print("-" * 60)

if __name__ == '__main__':
    print(LOGO)
    main()
