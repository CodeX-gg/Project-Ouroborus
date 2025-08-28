import os
import readline
from colorama import init as colorama_init, Fore, Style

# --- Import command registry and all command categories ---
from cmds.registry import (
    COMMANDS, COMMAND_META, 
    prompt, parse_input, print_command, 
    syntax_error, info, HISTORY_COLOR
)
import cmds.registry as registry  # for cwd, etc.

colorama_init(autoreset=True)

cwd = os.getcwd()
history = []

# --- Tab Completion (commands and files) ---
def complete(text, state):
    buffer = readline.get_line_buffer()
    tokens = parse_input(buffer)
    if len(tokens) <= 1:
        matches = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    else:
        try:
            partial = text or ''
            dir_part = os.path.dirname(partial)
            dir_part = os.path.join(registry.cwd, dir_part) if dir_part and not os.path.isabs(dir_part) else (dir_part or registry.cwd)
            prefix = os.path.basename(partial)
            items = os.listdir(dir_part)
            matches = [os.path.join(dir_part, item) for item in items if item.startswith(prefix)]
            matches = [m + (os.sep if os.path.isdir(os.path.join(dir_part, m)) else '') for m in matches]
            matches = [os.path.relpath(m, registry.cwd) for m in matches]
        except Exception:
            matches = []
    try:
        return matches[state]
    except IndexError:
        return None

readline.set_completer_delims(' \t\n')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def main():
    info(f"Ouroboros Terminal. Type {HISTORY_COLOR}help{Style.RESET_ALL} for a command list.")
    while True:
        try:
            os.chdir(registry.cwd)
            raw = input(prompt())
            if not raw.strip():
                continue
            print_command(raw)
            registry.history.append(raw)
            readline.add_history(raw)
            tokens = parse_input(raw)
            if not tokens:
                continue
            cmd, args = tokens[0], tokens[1:]
            if cmd in COMMANDS:
                COMMANDS[cmd](args)
            else:
                syntax_error(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("\n(Use 'exit' to quit)")
        except EOFError:
            print("\nSession closed.")
            break

if __name__ == "__main__":
    main()