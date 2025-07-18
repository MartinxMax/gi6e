from lib.GI6E import *

def shellcode_file_to_grid_string(filepath: str) -> str:
    namespace = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        exec(code, {}, namespace)
        sc = namespace.get("shellcode")
        if not isinstance(sc, (bytes, bytearray)):
            raise ValueError("`shellcode` variable not found or not bytes")
        return ''.join(f"{b:02x}" for b in sc)
    except Exception as e:
        exit(1)

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Convert raw shellcode to GI6E grid format')
    parser.add_argument('-key', type=str, help='Optional key (must be at least 8 characters)')
    parser.add_argument('-i', type=str, default='./SHELLCODE/Main.conf', help='Input shellcode python file')
    parser.add_argument('-o', type=str, default='./SHELLCODE/Main.grid', help='Output grid file path')
    args = parser.parse_args()

    if args.key and len(args.key) < 8:
        print("[!] Error: key must be at least 8 characters long.")
        sys.exit(1)

    g = grid()
    raw_hex = shellcode_file_to_grid_string(args.i)
    data, _ = g.text_2_grid(raw_hex, key=args.key) if args.key else g.text_2_grid(raw_hex)

    with open(args.o, 'w', encoding='utf-8') as f:
        f.write(f"'{data}'")

    print(f"[=] Conversion success:\n{data}")

