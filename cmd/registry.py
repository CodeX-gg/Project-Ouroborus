import os
import sys
import shlex
import platform
import time
from colorama import Fore, Style

# --- Global State ---
USER = os.environ.get("USERNAME") or os.environ.get("USER") or "user"
HOME = os.path.expanduser("~")
cwd = os.getcwd()
history = []
COMMANDS = {}
COMMAND_META = {}

# --- Style constants ---
THEME_COLOR = Fore.LIGHTGREEN_EX
TITLE_COLOR = Fore.LIGHTWHITE_EX + Style.BRIGHT
SECTION_COLOR = Fore.LIGHTBLUE_EX + Style.BRIGHT
PROMPT_HANDLE = Fore.LIGHTGREEN_EX + Style.BRIGHT
PROMPT_PATH = Fore.LIGHTBLUE_EX + Style.BRIGHT
PROMPT_ARROW = Fore.LIGHTYELLOW_EX + Style.BRIGHT
INPUT_COLOR = Fore.LIGHTCYAN_EX + Style.BRIGHT
OUTPUT_COLOR = Fore.LIGHTWHITE_EX + Style.NORMAL
ERROR_COLOR = Fore.LIGHTRED_EX + Style.BRIGHT
SUCCESS_COLOR = Fore.LIGHTGREEN_EX + Style.BRIGHT
HISTORY_COLOR = Fore.LIGHTYELLOW_EX
SEPARATOR = Fore.LIGHTBLACK_EX + "─" * 72 + Style.RESET_ALL

def print_command(cmd):
    print(f"{INPUT_COLOR}{cmd}{Style.RESET_ALL}")

def prompt():
    global cwd
    path = cwd.replace(HOME, "~", 1)
    return f"{PROMPT_HANDLE}[{USER}@ouroboros {PROMPT_PATH}{path}{PROMPT_HANDLE}]{PROMPT_ARROW} λ {Style.RESET_ALL}"

def syntax_error(msg):
    print(f"{ERROR_COLOR}✖ {msg}{Style.RESET_ALL}")

def info(msg):
    print(f"{Fore.CYAN}➜ {msg}{Style.RESET_ALL}")

def success(msg):
    print(f"{SUCCESS_COLOR}✔ {msg}{Style.RESET_ALL}")

def section(title):
    print(f"\n{SECTION_COLOR}{title}{Style.RESET_ALL}")
    print(SEPARATOR)

def separator():
    print(SEPARATOR)

def register_command(name, desc, group="General"):
    def decorator(fn):
        COMMANDS[name] = fn
        COMMAND_META[name] = {"desc": desc, "group": group}
        return fn
    return decorator

def parse_input(raw):
    try:
        return shlex.split(raw)
    except Exception as e:
        syntax_error(f"Parsing error: {e}")
        return []

# --- Import all command categories ---
from . import filesystem, network, text, utility
from . import general  # help, exit, clear, history, repeat (must be last for help to see all commands)