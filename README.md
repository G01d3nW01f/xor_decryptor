# Repeating-Key XOR Decryption Tool

This is a simple Python3 utility for decrypting data encrypted with a **repeating-key XOR cipher**.
It supports both **single-key decryption** and **dictionary-based key testing** (wordlist mode).

The tool is designed to be flexible and CTF-friendly, without making any assumptions about
the decrypted output format.

---

## Features

* Repeating-key XOR decryption
* Accepts encrypted data stored as a Python `bytes` literal
* Single key mode (`--key`)
* Wordlist / dictionary mode (`--wordlist`)
* No automatic filtering or "KEY FOUND" heuristics
* Graceful handling of non-UTF-8 output

---

## Encrypted File Format

The encrypted file must contain a **Python bytes literal**, for example:

```
b' \x00\x00\x00\x00%\x1c\r\x03\x18\x06\x1e'
```

This format is commonly found in CTF challenges or Python-based encryption scripts.

---

## Usage

### 1. Decrypt with a single key

```bash
python3 decrypt.py --enc encrypted.txt --key ayham
```

Example output:

```
[KEY: ayham] AyhamDeebugg
```

---

### 2. Decrypt using a wordlist (dictionary attack)

```bash
python3 decrypt.py --enc encrypted.txt --wordlist keys.txt
```

Each line in `keys.txt` is treated as a candidate key.

Example output:

```
[KEY: test] �\x12��
[KEY: secret] HelloWorld
[KEY: ayham] AyhamDeebugg
```

The script does **not** stop automatically or try to guess which output is correct.

---

## Arguments

| Argument     | Description                              |
| ------------ | ---------------------------------------- |
| `--enc`      | Path to the encrypted file (required)    |
| `--key`      | XOR key as a string                      |
| `--wordlist` | Path to a file containing candidate keys |

> You must specify **either** `--key` **or** `--wordlist`, but not both.

---

## Example Wordlist

```
password
secret
admin
ayham
test123
```

---

## How It Works

* Loads the encrypted data using `ast.literal_eval`
* Applies repeating-key XOR:

  ```
  plaintext[i] = ciphertext[i] XOR key[i % len(key)]
  ```
* Attempts UTF-8 decoding
* Falls back to raw byte output if decoding fails

---

## Requirements

* Python 3.7+
* No external dependencies (standard library only)

---

## Use Cases

* CTF challenges
* XOR cipher analysis
* Malware or reverse engineering practice
* Educational cryptography experiments

---

## Disclaimer

This tool is intended for **educational and research purposes only**.
Do not use it on data you do not have permission to analyze.

---

## License

MIT License
