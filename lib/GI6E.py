#  \_________________/
#  __/___|_____|___\__      ---------
# /⭕⭕______⭕⭕\      |  S-H4CK13  |
# |__/__MAPTNH __\__|       ---------
# \©©__|_|_|_|_|__©©/         | |
#
#               HEXGRID-6
#  A,0,6   = 001 001 ; 001 010 ; 001 011
#  B,1,7   = 010 001 ; 010 010 ; 010 011
#  C,2,8   = 011 001 ; 011 010 ; 011 011
#  D,3,9   = 100 001 ; 100 010 ; 100 011
#  E,4,Null= 101 001 ; 101 010 ; 101 011
#  F,5,Null= 110 001 ; 110 010 ; 110 011

'''
@Maptnh Update 2025/7/16
HEX-GRID CODEX (abbreviated as HGC) is a custom 6-bit structured encoding system that utilizes a three-bit group identifier (Group Bits) plus a three-bit index identifier (Index Bits) to form 64 unique codes. Its core design philosophy maps letters and numbers onto a two-dimensional block matrix, enabling scalable, hierarchical, and machine-parsable character distribution. This makes it suitable for Morse code extensions, embedded communication protocols, cryptographic tagging, or compact representation of special character sequences.
'''

import wave
import math
import scipy.io.wavfile as wav
import struct
import time
import numpy as np
import questionary
import os
import string
import random
import soundcard as sc
from Crypto.Cipher import AES
NONCE = b'\x46\x55\x43\x4B\x59\x4F\x55\x30'


class aesCtr():

    def ctr_generate_random_key(self,length=8):
        chars = string.ascii_letters + string.digits  
        return ''.join(random.choice(chars) for _ in range(length))

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
        self.path = './lib/history/'
        self.__MORSE_REVERSE_DICT = {v: k for k, v in self.__MORSE_CODE_DICT.items()}
        self.sample_rate = 44100
        self.freq = 800  
        self.volume = 0.8
        self.unit_duration=0.04
 
    '''
    Convert plaintext into GRID code format, 
    with an option to generate a corresponding WAV audio file. 
    If enabled, the return value is a tuple: (GRID code string, 
    audio filename); 
    otherwise, only the GRID code string is returned.
    '''
    def text_2_grid(self,text:str,wav:bool=False,key:str=''):
        if key and (not len(key)>=8)   :return (False,False)
        def __hex_2_grid(hex_):
            hex_ = hex_.upper()
            grid_hex_ = []
            for c in hex_:  
                if c in self.__MORSE_CODE_DICT:
                    grid_hex_.append(self.__MORSE_CODE_DICT[c]+' . ')
            return grid_hex_
        hex_ = self.__str_2_hex_list(text)
        if key :
            if not (hex_ :=  self.aes.ctr_encrypt(key,hex_)):
                return (False,False)
        hex_ = __hex_2_grid(hex_)
        hex_.insert(0,(self.__MORSE_CODE_DICT['+']+' . '))
        if wav:
            filename = os.path.join(self.path, 'generate', f"{int(time.time())}.wav")
            self.__grid_2_wav(hex_,filename)
            return (''.join(hex_),filename)
        return (''.join(hex_),False)
 
    
    '''
    Convert GRID code (encoded as Morse) back into readable plaintext. 
    This involves stripping delimiters, 
    decoding each Morse segment into a hex string using a reverse lookup table, 
    and converting the hex string into a UTF-8 decoded plaintext.
    '''
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
  

    def __grid_2_wav(self, grid_code:list, filename:str ):
        def generate_tone(frequency, duration, volume=0.5):
            num_samples = int(self.sample_rate * duration)
            result = []
            for i in range(num_samples):
                sample = volume * math.sin(2 * math.pi * frequency * (i / self.sample_rate))
                packed_sample = struct.pack('<h', int(sample * 32767))
                result.append(packed_sample)
            return b''.join(result)

        def generate_silence(duration):
            num_samples = int(self.sample_rate * duration)
            return b'\x00\x00' * num_samples


        audio_data = b''
        for idx, symbol in enumerate(grid_code):
            for ch in symbol:
                if ch == '.':
                    audio_data += generate_tone(self.freq, self.unit_duration, self.volume)
                    audio_data += generate_silence(self.unit_duration)  
                elif ch == '-':
                    audio_data += generate_tone(self.freq, 5 * self.unit_duration, self.volume)
                    audio_data += generate_silence(self.unit_duration)
                elif ch == ' ':
                    audio_data += generate_silence(6 * self.unit_duration)

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)
        print(f"[+] Grid file successfully generated: {filename}")


    '''
    Convert WAV audio back into readable plaintext.  
    Requires providing the path to the WAV audio file.
    '''
    def wav_2_text(self,wav_path:str,key:str=''):
        if not wav_path:return False
        if key and (not len(key)>=8)  :return False
        def envelope(signal, rate, window_ms=10):
            window_size = int(rate * window_ms / 1000)
            return np.convolve(np.abs(signal),
                            np.ones(window_size)/window_size,
                            mode='same')
        def threshold_signal(env, thresh):
            return (env > thresh).astype(int)
        def extract_durations(bin_sig, rate):
            durations, current, count = [], bin_sig[0], 1
            for b in bin_sig[1:]:
                if b == current:
                    count += 1
                else:
                    durations.append((current, count/rate))
                    current, count = b, 1
            durations.append((current, count/rate))
            return durations

        def estimate_dot_length(durations):
            ones = [d for v,d in durations if v==1]
            if not ones: return None
            ones_sorted = sorted(ones)
            n = max(1, len(ones_sorted)//3)
            return np.median(ones_sorted[:n])

        def decode_grid(durations, dot_length):
            grid = ""
            for state, duration in durations:
                units = duration / dot_length 
                if state == 1:  
                    if units <= 1.5:
                        grid += '.'
                    else:
                        grid += '-'
                else: 
                    if units >= 3:
                        grid += ' '   
            return grid.strip()
        rate, data = wav.read(wav_path)
        if data.ndim > 1:
            data = data[:,0]
        env = envelope(data, rate)
        thresh = np.max(env) * 0.25
        bin_sig = threshold_signal(env, thresh)
        durations = extract_durations(bin_sig, rate)
        dot_length = estimate_dot_length(durations)
        grid = decode_grid(durations, dot_length)+' '
        grid_dec = self.grid_2_text(grid,key)
        # print('-'*100)
        # print(f"Estimated dot_length: {dot_length}")
        # print(f"Envelope max: {np.max(env)}, threshold used: {thresh}")
        # print(f"Durations sample count: {len(durations)}")
        # print(f"Grid decoded: {grid}")
        return (grid,grid_dec)


    '''
    Retrieve all available loopback audio devices (e.g., Stereo Mix or VB-Cable).  
    Returns a tuple: (list of displayable device names, corresponding microphone objects).  
    If no loopback devices are detected, prints a warning and returns None.
    '''
    def get_audio_list(self):
        lbs = sc.all_microphones(include_loopback=True)
        lbs = [m for m in lbs if m.isloopback]
        if not lbs:
            print("[!] No loopback device found. Please enable Stereo Mix or install VB-Cable.")
            return
        mic_list = [f"[{i}] {m.name}" for i, m in enumerate(lbs)]
        return (mic_list,lbs)


    '''
    Real-time listening on a selected loopback audio device. 
    Recording starts when signal energy exceeds the threshold and ends after 3 seconds of continuous silence. 
    Recorded audio is saved to ./<path>/receve/ with a timestamped filename (.wav),
    then automatically decoded from Morse-Grid to plaintext.
    Returns a tuple: (grid_code, decoded_text).
    '''
    def realtime_grid_detection(self,mic=False,threshold:float=0.01, block_size:float=2048,key:str=''):
        def choice_device_and_record():
            choices,lbs = self.get_audio_list()
            selected = questionary.select(
                '''
      _._     _,-'""`-._
     (,-.`._,'(       |\`-/|    --------------------------------------------------
         `-.-' \ )-`( , o o)  <  Please select a Loopback audio device to monitor |
     -MT-      `-    \`_`"'-    --------------------------------------------------
                ''',
                choices=choices
            ).ask()
            if not selected:
                print("[!] No device selected, exiting.")
                return
            idx = int(selected.split(']')[0][1:]) 
            mic = lbs[idx]
            return mic
        if not mic:
            mic = choice_device_and_record()
 
            
        print(f"[*] Initializing {mic.name} and starting loopback monitoring...")
        buffer_audio = []
        buffer_morse_bits = np.array([], dtype=int)
        recording = False
        history_sec = 5   
        max_bits = int(self.sample_rate * history_sec / block_size)

        silent_chunks = 0
        max_silence_chunks = int(3 * self.sample_rate / block_size)  
        print("[*] Acquiring signal...")
        with mic.recorder(samplerate=self.sample_rate, channels=1) as rec:
            try:
                while True:
                    data = rec.record(numframes=block_size)[:,0]
                    rms = np.sqrt(np.mean(data**2))
                    env = np.mean(np.abs(data))
                    bit = 1 if env > threshold else 0
                    buffer_morse_bits = np.append(buffer_morse_bits, bit)
                     
                    if len(buffer_morse_bits) > max_bits:
                        buffer_morse_bits = buffer_morse_bits[-max_bits:]
                    
                    if bit == 1 and not recording:
                        recording = True
                        buffer_audio.clear()
                        print("[+] Signal detected")

                    if recording:
                        buffer_audio.append(data.copy())
                        if bit == 0:
                            silent_chunks += 1
                            if silent_chunks >= max_silence_chunks:
                                print("[+] Signal acquisition ended")
                                break
                        else:
                            silent_chunks = 0

            except KeyboardInterrupt:
                print("[+] Signal acquisition ended")

        if recording and buffer_audio:
            audio = np.concatenate(buffer_audio)
            save_dir = self.path
            os.makedirs(save_dir, exist_ok=True)
            fn = os.path.join(save_dir, 'receve', f"{int(time.time())}.wav")
            wav.write(fn, self.sample_rate, (audio*32767).astype(np.int16))
            print(f"[+] Recording saved to {fn}")
            return self.wav_2_text(fn,key)
        else:
            print("[!] No recording was made")


    def __str_2_hex_list(self,text:str):
        return text.encode('utf-8').hex().upper()


    def __hex_string_2_str(self, hex_:str):
        try:
            return bytes.fromhex(hex_).decode('utf-8')
        except Exception:
            return False
