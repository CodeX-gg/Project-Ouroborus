from .registry import (
    register_command, TITLE_COLOR, SECTION_COLOR, HISTORY_COLOR, Style,
    COMMAND_META, COMMANDS, separator, syntax_error, success, info
)
import os
import sys
import platform
import time
import datetime
import random

@register_command("help", "Show all available commands.", "General")
def cmd_help(args):
    print(f"{TITLE_COLOR}\nOuroboros Terminal – Command Reference{Style.RESET_ALL}")
    groups = {}
    for cmd, meta in COMMAND_META.items():
        groups.setdefault(meta["group"], []).append((cmd, meta["desc"]))
    for group, cmds in sorted(groups.items()):
        print(f"{SECTION_COLOR}{group}{Style.RESET_ALL}")
        for cmd, desc in sorted(cmds):
            print(f"  {HISTORY_COLOR}{cmd:<15}{Style.RESET_ALL} {desc}")
        print()
    separator()

@register_command("clear", "Clear the terminal screen.", "General")
def cmd_clear(args):
    os.system('cls' if os.name == 'nt' else 'clear')

@register_command("exit", "Exit the terminal.", "General")
def cmd_exit(args):
    from .registry import SUCCESS_COLOR, Style
    print(f"{SUCCESS_COLOR}Session closed.{Style.RESET_ALL}")
    sys.exit(0)

@register_command("history", "Show recent command history.", "General")
def cmd_history(args):
    from .registry import history, HISTORY_COLOR, Style
    for i, cmd in enumerate(history[-30:], start=max(1, len(history)-29)):
        print(f"{HISTORY_COLOR}{i:>3}{Style.RESET_ALL}: {cmd}")

@register_command("repeat", "Repeat the last command.", "General")
def cmd_repeat(args):
    from .registry import history, print_command, parse_input, COMMANDS, syntax_error
    if history:
        last = history[-1]
        print_command(last)
        tokens = parse_input(last)
        if tokens:
            cmd, args = tokens[0], tokens[1:]
            if cmd in COMMANDS:
                COMMANDS[cmd](args)
            else:
                syntax_error(f"Unknown command: {cmd}")
    else:
        syntax_error("No command history.")

@register_command("about", "Show about info for Ouroboros Terminal.", "General")
def cmd_about(args):
    info("Ouroboros Terminal — a modular, extensible, Python-powered shell with style and power!")

@register_command("version", "Show terminal version and Python version.", "General")
def cmd_version(args):
    print(f"Ouroboros Terminal version: 1.0.0")
    print(f"Python version: {platform.python_version()}")

@register_command("calc", "Evaluate a math expression.", "General")
def cmd_calc(args):
    expr = input("Expression to calculate: ")
    try:
        result = eval(expr, {"__builtins__": {}})
        print(f"Result: {result}")
    except Exception as e:
        syntax_error(e)

@register_command("randompick", "Pick a random item from a comma-separated list.", "General")
def cmd_randompick(args):
    items = input("Enter items (comma separated): ").split(",")
    items = [item.strip() for item in items if item.strip()]
    if not items:
        syntax_error("No items given.")
        return
    print(f"Random pick: {random.choice(items)}")

@register_command("timer", "Set a simple countdown timer (seconds).", "General")
def cmd_timer(args):
    try:
        seconds = int(input("Seconds for countdown: "))
        for i in range(seconds, 0, -1):
            print(f"{i}...", end="\r")
            time.sleep(1)
        print("Time's up!          ")
    except Exception as e:
        syntax_error(e)

@register_command("stopwatch", "Start a basic stopwatch. Press Enter to stop.", "General")
def cmd_stopwatch(args):
    input("Press Enter to start stopwatch...")
    start = time.time()
    input("Press Enter to stop stopwatch...")
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f} seconds")

@register_command("date", "Show current date.", "General")
def cmd_date(args):
    print(datetime.date.today().strftime("%Y-%m-%d"))

@register_command("time", "Show current time.", "General")
def cmd_time(args):
    print(datetime.datetime.now().strftime("%H:%M:%S"))

@register_command("sleep", "Pause execution for N seconds.", "General")
def cmd_sleep(args):
    try:
        sec = int(input("How many seconds to sleep? "))
        time.sleep(sec)
        print("Done sleeping.")
    except Exception as e:
        syntax_error(e)

@register_command("repeatprint", "Print a line multiple times.", "General")
def cmd_repeatprint(args):
    line = input("Text to print: ")
    try:
        count = int(input("How many times? "))
        for _ in range(count):
            print(line)
    except Exception as e:
        syntax_error(e)

@register_command("echo", "Echo back your input.", "General")
def cmd_echo(args):
    text = input("Say something: ")
    print(text)

@register_command("yes", "Prints 'y' repeatedly (press Ctrl+C to stop).", "General")
def cmd_yes(args):
    try:
        while True:
            print("y")
    except KeyboardInterrupt:
        print()

@register_command("choose", "Choose between two options.", "General")
def cmd_choose(args):
    a = input("Option 1: ")
    b = input("Option 2: ")
    print(f"Chosen: {random.choice([a, b])}")

@register_command("flip", "Flip a coin.", "General")
def cmd_flip(args):
    print(random.choice(["Heads", "Tails"]))

@register_command("roll", "Roll an N-sided die.", "General")
def cmd_roll(args):
    try:
        sides = int(input("How many sides? "))
        print(f"Roll: {random.randint(1, sides)}")
    except Exception as e:
        syntax_error(e)

@register_command("greet", "Greet yourself or a name.", "General")
def cmd_greet(args):
    name = input("Enter your name: ")
    print(f"Hello, {name}! Welcome to Ouroboros Terminal.")

@register_command("repeatinput", "Ask for input N times.", "General")
def cmd_repeatinput(args):
    try:
        count = int(input("How many times? "))
        for i in range(count):
            val = input(f"Input #{i+1}: ")
            print(f"You said: {val}")
    except Exception as e:
        syntax_error(e)