import random
import base64
import hashlib
import pyperclip
import string
from colorama import Fore, Style
from .registry import (
    register_command, OUTPUT_COLOR, syntax_error, success, section
)

@register_command("uuid", "Generate a random UUID.", "Text/Encoding")
def cmd_uuid(args):
    import uuid
    print(f"{Fore.LIGHTYELLOW_EX}UUID:{Style.RESET_ALL} {str(uuid.uuid4())}")

@register_command("password", "Generate a strong random password.", "Text/Encoding")
def cmd_password(args):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    length = int(input("Password length: "))
    pwd = ''.join(random.choice(chars) for _ in range(length))
    print(f"{Fore.LIGHTYELLOW_EX}Random Password:{Style.RESET_ALL} {pwd}")

@register_command("base64", "Encode/decode base64.", "Text/Encoding")
def cmd_base64(args):
    mode = input("Encode or decode? ").strip().lower()
    text = input("Text: ")
    if mode == "encode":
        out = base64.b64encode(text.encode()).decode()
        print(f"{Fore.LIGHTYELLOW_EX}Base64:{Style.RESET_ALL} {out}")
    elif mode == "decode":
        try:
            out = base64.b64decode(text.encode()).decode()
            print(f"{Fore.LIGHTYELLOW_EX}Decoded:{Style.RESET_ALL} {out}")
        except:
            syntax_error("Invalid base64 input.")
    else:
        syntax_error("Unknown mode.")

@register_command("sha256", "SHA256 hash of text.", "Text/Encoding")
def cmd_sha256(args):
    txt = input("Text: ")
    hashval = hashlib.sha256(txt.encode()).hexdigest()
    print(f"{Fore.LIGHTYELLOW_EX}SHA-256:{Style.RESET_ALL} {hashval}")

@register_command("sha1", "SHA1 hash of text.", "Text/Encoding")
def cmd_sha1(args):
    txt = input("Text: ")
    hashval = hashlib.sha1(txt.encode()).hexdigest()
    print(f"{Fore.LIGHTYELLOW_EX}SHA-1:{Style.RESET_ALL} {hashval}")

@register_command("md5", "MD5 hash of text.", "Text/Encoding")
def cmd_md5(args):
    txt = input("Text: ")
    hashval = hashlib.md5(txt.encode()).hexdigest()
    print(f"{Fore.LIGHTYELLOW_EX}MD5:{Style.RESET_ALL} {hashval}")

@register_command("hex", "Convert text to hex.", "Text/Encoding")
def cmd_hex(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Hex:{Style.RESET_ALL} {txt.encode().hex()}")

@register_command("unhex", "Convert hex to text.", "Text/Encoding")
def cmd_unhex(args):
    h = input("Hex: ")
    try:
        print(f"{Fore.LIGHTYELLOW_EX}Decoded:{Style.RESET_ALL} {bytes.fromhex(h).decode()}")
    except:
        syntax_error("Invalid hex input.")

@register_command("random", "Random number in a range.", "Text/Encoding")
def cmd_random(args):
    lo = int(input("Min: "))
    hi = int(input("Max: "))
    print(f"{Fore.LIGHTYELLOW_EX}Random:{Style.RESET_ALL} {random.randint(lo, hi)}")

@register_command("copyclip", "Copy text to clipboard.", "Text/Encoding")
def cmd_copyclip(args):
    txt = input("Copy text: ")
    pyperclip.copy(txt)
    success("Copied to clipboard.")

@register_command("pasteclip", "Paste text from clipboard.", "Text/Encoding")
def cmd_pasteclip(args):
    txt = pyperclip.paste()
    print(f"{Fore.LIGHTYELLOW_EX}Clipboard:{Style.RESET_ALL} {txt}")

@register_command("reverse", "Reverse a string.", "Text/Encoding")
def cmd_reverse(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Reversed:{Style.RESET_ALL} {txt[::-1]}")

@register_command("capitalize", "Capitalize string.", "Text/Encoding")
def cmd_capitalize(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Capitalized:{Style.RESET_ALL} {txt.capitalize()}")

@register_command("upper", "Convert text to uppercase.", "Text/Encoding")
def cmd_upper(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Uppercase:{Style.RESET_ALL} {txt.upper()}")

@register_command("lower", "Convert text to lowercase.", "Text/Encoding")
def cmd_lower(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Lowercase:{Style.RESET_ALL} {txt.lower()}")

@register_command("title", "Title-case a string.", "Text/Encoding")
def cmd_title(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Title Case:{Style.RESET_ALL} {txt.title()}")

@register_command("count", "Count substring in string.", "Text/Encoding")
def cmd_count(args):
    txt = input("Text: ")
    sub = input("Substring to count: ")
    print(f"{Fore.LIGHTYELLOW_EX}Count:{Style.RESET_ALL} {txt.count(sub)}")

@register_command("replace", "Replace substring in string.", "Text/Encoding")
def cmd_replace(args):
    txt = input("Text: ")
    old = input("Replace what? ")
    new = input("Replace with? ")
    print(f"{Fore.LIGHTYELLOW_EX}Result:{Style.RESET_ALL} {txt.replace(old, new)}")

@register_command("strip", "Strip whitespace from string.", "Text/Encoding")
def cmd_strip(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Stripped:{Style.RESET_ALL} {txt.strip()}")

@register_command("split", "Split string by separator.", "Text/Encoding")
def cmd_split(args):
    txt = input("Text: ")
    sep = input("Separator (blank for whitespace): ")
    result = txt.split(sep) if sep else txt.split()
    print(f"{Fore.LIGHTYELLOW_EX}Split:{Style.RESET_ALL} {result}")

@register_command("join", "Join a list of strings.", "Text/Encoding")
def cmd_join(args):
    items = input("Enter items (comma separated): ").split(",")
    sep = input("Separator: ")
    print(f"{Fore.LIGHTYELLOW_EX}Joined:{Style.RESET_ALL} {sep.join(items)}")

@register_command("caesar", "Caesar cipher encode/decode.", "Text/Encoding")
def cmd_caesar(args):
    mode = input("Encode or decode? ").strip().lower()
    txt = input("Text: ")
    try:
        shift = int(input("Shift (e.g. 3): "))
    except ValueError:
        syntax_error("Invalid shift value.")
        return
    def caesar(text, shift_val):
        res = ""
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                res += chr((ord(c) - base + shift_val) % 26 + base)
            else:
                res += c
        return res
    if mode == "encode":
        print(f"{Fore.LIGHTYELLOW_EX}Encoded:{Style.RESET_ALL} {caesar(txt, shift)}")
    elif mode == "decode":
        print(f"{Fore.LIGHTYELLOW_EX}Decoded:{Style.RESET_ALL} {caesar(txt, -shift)}")
    else:
        syntax_error("Unknown mode.")

@register_command("palindrome", "Check if a string is a palindrome.", "Text/Encoding")
def cmd_palindrome(args):
    txt = input("Text: ")
    is_pal = txt == txt[::-1]
    print(f"{Fore.LIGHTYELLOW_EX}Palindrome:{Style.RESET_ALL} {'Yes' if is_pal else 'No'}")

@register_command("anagram", "Check if two strings are anagrams.", "Text/Encoding")
def cmd_anagram(args):
    a = input("First string: ")
    b = input("Second string: ")
    is_ana = sorted(a.replace(" ", "")) == sorted(b.replace(" ", ""))
    print(f"{Fore.LIGHTYELLOW_EX}Anagram:{Style.RESET_ALL} {'Yes' if is_ana else 'No'}")

@register_command("wordcount", "Count words in string.", "Text/Encoding")
def cmd_wordcount(args):
    txt = input("Text: ")
    count = len(txt.split())
    print(f"{Fore.LIGHTYELLOW_EX}Word count:{Style.RESET_ALL} {count}")

@register_command("charcount", "Count characters in string.", "Text/Encoding")
def cmd_charcount(args):
    txt = input("Text: ")
    print(f"{Fore.LIGHTYELLOW_EX}Character count:{Style.RESET_ALL} {len(txt)}")