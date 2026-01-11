#!/usr/bin/python3

import argparse
import ast
import sys

def xor_dcrypt(ciphertxt: bytes, key: str) -> bytearray:
    dcrypt_msg = bytearray()
    for i in range(len(ciphertxt)):
        dcrypt_byte = ciphertxt[i] ^ ord(key[i % len(key)])
        dcrypt_msg.append(dcrypt_byte)
    return dcrypt_msg

def load_encrypted_file(path: str) -> bytes:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except IOError as e:
        print(f"[!] File error: {e}")
        sys.exit(1)

    try:
        data = ast.literal_eval(content)
    except Exception:
        print("[!] Invalid encrypted file format")
        print("[!] Expected format: b'\\x01\\x02...'")
        sys.exit(1)

    if not isinstance(data, (bytes, bytearray)):
        print("[!] Encrypted data is not bytes")
        sys.exit(1)

    return bytes(data)

def load_wordlist(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                key = line.rstrip("\n")
                if key:
                    yield key
    except IOError as e:
        print(f"[!] Wordlist error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Repeating-key XOR decryption tool (no filtering)"
    )
    parser.add_argument("--enc", required=True, help="Encrypted file path")
    parser.add_argument("--key", help="XOR key (string)")
    parser.add_argument("--wordlist", help="Key wordlist file")

    args = parser.parse_args()

    if not args.key and not args.wordlist:
        print("[!] Either --key or --wordlist must be specified")
        sys.exit(1)

    if args.key and args.wordlist:
        print("[!] Use only one of --key or --wordlist")
        sys.exit(1)

    encrypted = load_encrypted_file(args.enc)

    # single key 
    if args.key:
        decrypted = xor_dcrypt(encrypted, args.key)
        try:
            print(f"[KEY: {args.key}] {decrypted.decode('utf-8')}")
        except UnicodeDecodeError:
            print(f"[KEY: {args.key}] {decrypted}")

    # dictionary attack
    else:
        for key in load_wordlist(args.wordlist):
            decrypted = xor_dcrypt(encrypted, key)
            try:
                print(f"[KEY: {key}] {decrypted.decode('utf-8')}")
            except UnicodeDecodeError:
                print(f"[KEY: {key}] {decrypted}")

if __name__ == "__main__":
    main()

