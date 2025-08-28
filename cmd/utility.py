import os
import time
from colorama import Fore, Style
from .registry import (
    register_command, OUTPUT_COLOR, syntax_error, success
)

@register_command("open", "Open a file/folder with default app.", "Utility")
def cmd_open(args):
    import sys
    from . import registry
    if not args:
        fname = input("File/folder to open: ").strip()
    else:
        fname = args[0]
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        if os.name == "nt":
            os.startfile(path)
        elif sys.platform == "darwin":
            import subprocess
            subprocess.run(["open", path])
        else:
            import subprocess
            subprocess.run(["xdg-open", path])
        success(f"Opened {path}")
    except Exception as e:
        syntax_error(e)

@register_command("timer", "Start a countdown timer.", "Utility")
def cmd_timer(args):
    try:
        seconds = int(args[0]) if args else int(input("Seconds: "))
        for i in range(seconds, 0, -1):
            print(f"{Fore.LIGHTCYAN_EX} {i}...{Style.RESET_ALL}", end="\r")
            time.sleep(1)
        print(f"{Fore.LIGHTGREEN_EX}Time's up!{Style.RESET_ALL}{' '*10}")
    except Exception as e:
        syntax_error(e)

@register_command("calendar", "Show this month's calendar.", "Utility")
def cmd_calendar(args):
    import datetime
    import calendar
    now = datetime.datetime.now()
    cal = calendar.month(now.year, now.month)
    print(f"{Fore.LIGHTYELLOW_EX}{cal}{Style.RESET_ALL}")

@register_command("calc", "Calculate a math expression.", "Utility")
def cmd_calc(args):
    expr = " ".join(args) if args else input("Expression: ")
    try:
        result = eval(expr, {"__builtins__": {}})
        print(f"{Fore.LIGHTYELLOW_EX}Result:{Style.RESET_ALL} {result}")
    except Exception as e:
        syntax_error(e)

# New Utility Commands:

@register_command("date", "Display the current date.", "Utility")
def cmd_date(args):
    """Shows the current date."""
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"{Fore.LIGHTCYAN_EX}{current_date}{Style.RESET_ALL}")

@register_command("countdown", "Start a countdown timer with a custom message.", "Utility")
def cmd_countdown(args):
    """Start a countdown timer with a custom message."""
    try:
        if len(args) < 2:
            raise ValueError("You must provide both seconds and a message.")
        seconds = int(args[0])
        message = " ".join(args[1:])
        for i in range(seconds, 0, -1):
            print(f"{Fore.LIGHTCYAN_EX}{i}... {message}{Style.RESET_ALL}", end="\r")
            time.sleep(1)
        print(f"{Fore.LIGHTGREEN_EX}{message} Time's up!{Style.RESET_ALL}{' '*10}")
    except Exception as e:
        syntax_error(e)

@register_command("timezone", "Display the current time zone.", "Utility")
def cmd_timezone(args):
    """Displays the current system's time zone."""
    import time
    current_timezone = time.tzname[0]
    print(f"{Fore.LIGHTCYAN_EX}Timezone:{Style.RESET_ALL} {current_timezone}")

@register_command("encode", "Encode a string using a custom substitution cipher.", "Utility")
def cmd_encode(args):
    """Encodes a string using a substitution cipher (A=P, a=o, etc.)."""
    if not args:
        text = input("String to encode: ").strip()
    else:
        text = " ".join(args)
    
    # Define the substitution cipher for lowercase, uppercase, numbers, and symbols
    encoding_map = {
        'a': 'o', 'b': 'p', 'c': 'q', 'd': 'r', 'e': 's', 'f': 't', 'g': 'u', 'h': 'v', 'i': 'w', 'j': 'x', 'k': 'y', 'l': 'z', 'm': 'a', 
        'n': 'b', 'o': 'c', 'p': 'd', 'q': 'e', 'r': 'f', 's': 'g', 't': 'h', 'u': 'i', 'v': 'j', 'w': 'k', 'x': 'l', 'y': 'm', 'z': 'n',
        'A': 'P', 'B': 'Q', 'C': 'R', 'D': 'S', 'E': 'T', 'F': 'U', 'G': 'V', 'H': 'W', 'I': 'X', 'J': 'Y', 'K': 'Z', 'L': 'A', 'M': 'B', 
        'N': 'C', 'O': 'D', 'P': 'E', 'Q': 'F', 'R': 'G', 'S': 'H', 'T': 'I', 'U': 'J', 'V': 'K', 'W': 'L', 'X': 'M', 'Y': 'N', 'Z': 'O',
        '0': '9', '1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7', '9': '8',
        '!': '@', '@': '#', '#': '$', '$': '%', '%': '^', '^': '&', '&': '*', '*': '(', '(': ')', ')': '_', '_': '+', '+': '{', '{': '}', 
        '}': '[', '[': ']', ']': '|', '|': ';', ';': ':', ':': '"', '"': "'", "'": ',', ',': '.', '.': '?', '?': '/', '/': '\\', '\\': '=', 
        '=': '`', '`': '~'
    }

    encoded_text = ''.join([encoding_map.get(c, c) for c in text])  # Apply the cipher
    print(f"{Fore.LIGHTCYAN_EX}Encoded:{Style.RESET_ALL} {encoded_text}")


@register_command("decode", "Decode a string using the reverse of the custom encoding map.", "Utility")
def cmd_decode(args):
    """Decodes a string using the reverse of the substitution cipher."""
    if not args:
        text = input("String to decode: ").strip()
    else:
        text = " ".join(args)
    
    # Define the reverse of the substitution cipher
    decoding_map = {v: k for k, v in {
        'a': 'o', 'b': 'p', 'c': 'q', 'd': 'r', 'e': 's', 'f': 't', 'g': 'u', 'h': 'v', 'i': 'w', 'j': 'x', 'k': 'y', 'l': 'z', 'm': 'a', 
        'n': 'b', 'o': 'c', 'p': 'd', 'q': 'e', 'r': 'f', 's': 'g', 't': 'h', 'u': 'i', 'v': 'j', 'w': 'k', 'x': 'l', 'y': 'm', 'z': 'n',
        'A': 'P', 'B': 'Q', 'C': 'R', 'D': 'S', 'E': 'T', 'F': 'U', 'G': 'V', 'H': 'W', 'I': 'X', 'J': 'Y', 'K': 'Z', 'L': 'A', 'M': 'B', 
        'N': 'C', 'O': 'D', 'P': 'E', 'Q': 'F', 'R': 'G', 'S': 'H', 'T': 'I', 'U': 'J', 'V': 'K', 'W': 'L', 'X': 'M', 'Y': 'N', 'Z': 'O',
        '0': '9', '1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7', '9': '8',
        '!': '@', '@': '#', '#': '$', '$': '%', '%': '^', '^': '&', '&': '*', '*': '(', '(': ')', ')': '_', '_': '+', '+': '{', '{': '}', 
        '}': '[', '[': ']', ']': '|', '|': ';', ';': ':', ':': '"', '"': "'", "'": ',', ',': '.', '.': '?', '?': '/', '/': '\\', '\\': '=', 
        '=': '`', '`': '~'
    }.items()}  # Reverse the map

    decoded_text = ''.join([decoding_map.get(c, c) for c in text])  # Apply the reverse cipher
    print(f"{Fore.LIGHTCYAN_EX}Decoded:{Style.RESET_ALL} {decoded_text}")
