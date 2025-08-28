import os
import shutil
import glob
import fnmatch
import stat
import datetime
from colorama import Fore, Style
from .registry import (
    register_command, cwd, HOME, print_command, syntax_error, success, section, separator, OUTPUT_COLOR
)

@register_command("ls", "List files and folders.", "Filesystem")
def cmd_ls(args):
    global cwd
    show_all = "-a" in args
    long_format = "-l" in args
    target = args[-1] if args and not args[-1].startswith('-') else cwd
    target = os.path.expanduser(target)
    if not os.path.isabs(target):
        target = os.path.join(cwd, target)
    try:
        items = sorted(os.listdir(target))
        if long_format:
            section("Detailed Directory Listing")
            for item in items:
                if not show_all and item.startswith('.'):
                    continue
                full = os.path.join(target, item)
                info = os.stat(full)
                perms = stat.filemode(info.st_mode)
                size = info.st_size
                mtime = datetime.datetime.fromtimestamp(info.st_mtime).strftime("%Y-%m-%d %H:%M")
                color = Fore.LIGHTBLUE_EX if os.path.isdir(full) else Fore.LIGHTWHITE_EX
                print(f"{perms} {size:>8} {mtime} {color}{item}{Style.RESET_ALL}")
        else:
            for item in items:
                if not show_all and item.startswith('.'):
                    continue
                full = os.path.join(target, item)
                if os.path.isdir(full):
                    print(f"{Fore.LIGHTBLUE_EX}{item}{os.sep}{Style.RESET_ALL}", end="  ")
                elif os.access(full, os.X_OK):
                    print(f"{Fore.LIGHTGREEN_EX}{item}{Style.RESET_ALL}", end="  ")
                else:
                    print(f"{Fore.LIGHTWHITE_EX}{item}{Style.RESET_ALL}", end="  ")
            print()
    except Exception as e:
        syntax_error(e)

@register_command("cd", "Change working directory.", "Filesystem")
def cmd_cd(args):
    from . import registry
    if not args:
        path = HOME
    else:
        path = os.path.expanduser(args[0])
        if not os.path.isabs(path):
            path = os.path.join(registry.cwd, path)
    if os.path.isdir(path):
        registry.cwd = os.path.normpath(path)
    else:
        syntax_error(f'No such directory: "{args[0] if args else HOME}"')

@register_command("pwd", "Show the current directory.", "Filesystem")
def cmd_pwd(args):
    from . import registry
    print(f"{OUTPUT_COLOR}{registry.cwd}{Style.RESET_ALL}")

@register_command("cat", "Print contents of a file.", "Filesystem")
def cmd_cat(args):
    from . import registry
    if not args:
        filename = input("File: ").strip().strip('"')
    else:
        filename = args[0]
    path = os.path.expanduser(filename)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f"{OUTPUT_COLOR}{f.read()}{Style.RESET_ALL}")
    except Exception as e:
        syntax_error(e)

@register_command("touch", "Create an empty file.", "Filesystem")
def cmd_touch(args):
    from . import registry
    if not args:
        name = input("File name: ").strip().strip('"')
    else:
        name = args[0]
    path = os.path.expanduser(name)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        with open(path, "a", encoding="utf-8"):
            os.utime(path, None)
        success(f'Created {os.path.basename(path)}')
    except Exception as e:
        syntax_error(e)

@register_command("write", "Write text to a file.", "Filesystem")
def cmd_write(args):
    from . import registry
    if not args:
        fname = input("File to write: ").strip().strip('"')
    else:
        fname = args[0]
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    print("Enter text ('.' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        success(f'Wrote to {os.path.basename(path)}')
    except Exception as e:
        syntax_error(e)

@register_command("append", "Append text to a file.", "Filesystem")
def cmd_append(args):
    from . import registry
    if not args:
        fname = input("File to append to: ").strip().strip('"')
    else:
        fname = args[0]
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    print("Enter text to append ('.' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        success(f'Appended to {os.path.basename(path)}')
    except Exception as e:
        syntax_error(e)

@register_command("mkdir", "Create a new directory.", "Filesystem")
def cmd_mkdir(args):
    from . import registry
    if not args:
        name = input("Directory name: ").strip().strip('"')
    else:
        name = args[0]
    path = os.path.expanduser(name)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        os.makedirs(path, exist_ok=False)
        success(f'Created directory {os.path.basename(path)}')
    except Exception as e:
        syntax_error(e)

@register_command("rm", "Delete a file.", "Filesystem")
def cmd_rm(args):
    from . import registry
    if not args:
        fname = input("File to delete: ").strip().strip('"')
    else:
        fname = args[0]
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        os.remove(path)
        success(f'Removed {os.path.basename(path)}')
    except Exception as e:
        syntax_error(e)

@register_command("rmdir", "Delete a directory.", "Filesystem")
def cmd_rmdir(args):
    from . import registry
    if not args:
        name = input("Directory to delete: ").strip().strip('"')
    else:
        name = args[0]
    path = os.path.expanduser(name)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        os.rmdir(path)
        success(f'Removed directory {os.path.basename(path)}')
    except Exception as e:
        syntax_error(e)

@register_command("rmrf", "Recursively delete a directory (dangerous!).", "Filesystem")
def cmd_rmrf(args):
    from . import registry
    if not args:
        name = input("Directory to recursively delete: ").strip().strip('"')
    else:
        name = args[0]
    path = os.path.expanduser(name)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    confirm = input(f"Are you sure you want to recursively delete {path}? (yes/no): ")
    if confirm.lower() == "yes":
        try:
            shutil.rmtree(path)
            success(f"Recursively removed {os.path.basename(path)}")
        except Exception as e:
            syntax_error(e)
    else:
        print("Cancelled.")

@register_command("copy", "Copy a file.", "Filesystem")
def cmd_copy(args):
    from . import registry
    if len(args) < 2:
        src = input("Source file: ").strip().strip('"')
        dst = input("Destination path: ").strip().strip('"')
    else:
        src, dst = args[0], args[1]
    src_path = os.path.expanduser(src)
    dst_path = os.path.expanduser(dst)
    if not os.path.isabs(src_path):
        src_path = os.path.join(registry.cwd, src_path)
    if not os.path.isabs(dst_path):
        dst_path = os.path.join(registry.cwd, dst_path)
    try:
        shutil.copy2(src_path, dst_path)
        success(f"Copied {os.path.basename(src_path)} to {os.path.basename(dst_path)}")
    except Exception as e:
        syntax_error(e)

@register_command("move", "Move/rename a file or directory.", "Filesystem")
def cmd_move(args):
    from . import registry
    if len(args) < 2:
        src = input("Source file/dir: ").strip().strip('"')
        dst = input("Destination path: ").strip().strip('"')
    else:
        src, dst = args[0], args[1]
    src_path = os.path.expanduser(src)
    dst_path = os.path.expanduser(dst)
    if not os.path.isabs(src_path):
        src_path = os.path.join(registry.cwd, src_path)
    if not os.path.isabs(dst_path):
        dst_path = os.path.join(registry.cwd, dst_path)
    try:
        shutil.move(src_path, dst_path)
        success(f"Moved {os.path.basename(src_path)} to {os.path.basename(dst_path)}")
    except Exception as e:
        syntax_error(e)

@register_command("rename", "Rename a file or directory.", "Filesystem")
def cmd_rename(args):
    from . import registry
    old = input("Old name: ").strip().strip('"')
    new = input("New name: ").strip().strip('"')
    old_path = os.path.expanduser(old)
    new_path = os.path.expanduser(new)
    if not os.path.isabs(old_path):
        old_path = os.path.join(registry.cwd, old_path)
    if not os.path.isabs(new_path):
        new_path = os.path.join(registry.cwd, new_path)
    try:
        os.rename(old_path, new_path)
        success(f"Renamed {os.path.basename(old_path)} to {os.path.basename(new_path)}")
    except Exception as e:
        syntax_error(e)

@register_command("search", "Search for files/folders by name.", "Filesystem")
def cmd_search(args):
    from . import registry
    name = input("Search for (name or pattern, e.g. *.py): ").strip()
    results = []
    for root, dirs, files in os.walk(registry.cwd):
        for fname in files + dirs:
            if fnmatch.fnmatch(fname, name):
                results.append(os.path.join(root, fname))
    if results:
        print(f"{Fore.LIGHTYELLOW_EX}Found:{Style.RESET_ALL}")
        for r in results:
            print(f"  {Fore.LIGHTBLUE_EX}{r}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTRED_EX}No matches.{Style.RESET_ALL}")

@register_command("find", "Find files/folders recursively by glob pattern.", "Filesystem")
def cmd_find(args):
    from . import registry
    pattern = input("Pattern (e.g. **/*.txt): ").strip()
    results = glob.glob(os.path.join(registry.cwd, pattern), recursive=True)
    if results:
        print(f"{Fore.LIGHTYELLOW_EX}Found:{Style.RESET_ALL}")
        for r in results:
            print(f"  {Fore.LIGHTBLUE_EX}{r}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTRED_EX}No matches.{Style.RESET_ALL}")

@register_command("filesize", "Show size of a file in bytes/kb/mb.", "Filesystem")
def cmd_filesize(args):
    from . import registry
    fname = input("File: ").strip()
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        size = os.path.getsize(path)
        for unit in ['B','KB','MB','GB','TB']:
            if size < 1024.0:
                print(f"{Fore.LIGHTYELLOW_EX}Size:{Style.RESET_ALL} {size:.2f} {unit}")
                break
            size /= 1024.0
    except Exception as e:
        syntax_error(e)

@register_command("du", "Show total disk usage under a directory.", "Filesystem")
def cmd_du(args):
    from . import registry
    target = input("Directory to measure: ").strip() or registry.cwd
    path = os.path.expanduser(target)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    for unit in ['B','KB','MB','GB','TB']:
        if total < 1024.0:
            print(f"{Fore.LIGHTYELLOW_EX}Total size:{Style.RESET_ALL} {total:.2f} {unit}")
            break
        total /= 1024.0

@register_command("wc", "Count lines, words, and characters in a file.", "Filesystem")
def cmd_wc(args):
    from . import registry
    fname = input("File: ").strip()
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        lines = text.count('\n')
        words = len(text.split())
        chars = len(text)
        print(f"{Fore.LIGHTYELLOW_EX}Lines:{Style.RESET_ALL} {lines}")
        print(f"{Fore.LIGHTYELLOW_EX}Words:{Style.RESET_ALL} {words}")
        print(f"{Fore.LIGHTYELLOW_EX}Chars:{Style.RESET_ALL} {chars}")
    except Exception as e:
        syntax_error(e)

@register_command("head", "Show the first N lines of a file.", "Filesystem")
def cmd_head(args):
    from . import registry
    fname = input("File: ").strip()
    n = int(input("How many lines? "))
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= n:
                    break
                print(line.rstrip())
    except Exception as e:
        syntax_error(e)

@register_command("tail", "Show the last N lines of a file.", "Filesystem")
def cmd_tail(args):
    from . import registry
    fname = input("File: ").strip()
    n = int(input("How many lines? "))
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-n:]:
                print(line.rstrip())
    except Exception as e:
        syntax_error(e)

@register_command("chmod", "Change file permissions (numeric, e.g. 644).", "Filesystem")
def cmd_chmod(args):
    from . import registry
    fname = input("File: ").strip()
    perms = input("Permissions (octal, e.g. 644): ").strip()
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        os.chmod(path, int(perms, 8))
        success(f"Permissions of {os.path.basename(path)} changed to {perms}")
    except Exception as e:
        syntax_error(e)

@register_command("zip", "Compress a file or directory to .zip.", "Filesystem")
def cmd_zip(args):
    from . import registry
    import zipfile
    src = input("File/Directory to zip: ").strip()
    dest = input("Destination zip file: ").strip()
    src_path = os.path.expanduser(src)
    if not os.path.isabs(src_path):
        src_path = os.path.join(registry.cwd, src_path)
    try:
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
            if os.path.isdir(src_path):
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(src_path))
                        zf.write(file_path, arcname)
            else:
                zf.write(src_path, arcname=os.path.basename(src_path))
        success(f"Compressed {src} to {dest}")
    except Exception as e:
        syntax_error(e)

@register_command("unzip", "Extract files from a .zip file.", "Filesystem")
def cmd_unzip(args):
    from . import registry
    import zipfile
    src = input("Zip file to extract: ").strip()
    dest = input("Destination folder: ").strip()
    src_path = os.path.expanduser(src)
    if not os.path.isabs(src_path):
        src_path = os.path.join(registry.cwd, src_path)
    try:
        with zipfile.ZipFile(src_path, 'r') as zf:
            zf.extractall(dest)
        success(f"Extracted {src} to {dest}")
    except Exception as e:
        syntax_error(e)

@register_command("stat", "Show detailed status of a file.", "Filesystem")
def cmd_stat(args):
    from . import registry
    fname = input("File: ").strip()
    path = os.path.expanduser(fname)
    if not os.path.isabs(path):
        path = os.path.join(registry.cwd, path)
    try:
        info = os.stat(path)
        print(f"{Fore.LIGHTYELLOW_EX}Size:{Style.RESET_ALL} {info.st_size} bytes")
        print(f"{Fore.LIGHTYELLOW_EX}Permissions:{Style.RESET_ALL} {stat.filemode(info.st_mode)}")
        print(f"{Fore.LIGHTYELLOW_EX}Owner UID:{Style.RESET_ALL} {info.st_uid}")
        print(f"{Fore.LIGHTYELLOW_EX}Group GID:{Style.RESET_ALL} {info.st_gid}")
        print(f"{Fore.LIGHTYELLOW_EX}Last modified:{Style.RESET_ALL} {datetime.datetime.fromtimestamp(info.st_mtime)}")
        print(f"{Fore.LIGHTYELLOW_EX}Created:{Style.RESET_ALL} {datetime.datetime.fromtimestamp(info.st_ctime)}")
    except Exception as e:
        syntax_error(e)