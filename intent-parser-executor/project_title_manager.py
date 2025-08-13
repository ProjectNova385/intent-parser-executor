import os
import re
import ast
from datetime import datetime

# === your_project_title_here Intent Manager ===
# This script reads intents from 'your_project_title_here_intents.txt'
# code files. Supports commands: modify, insert, delete, append, replace.
# It includes safety checks and backup creation before modifying files.

intent_file = "your_project_title_here_intents.txt"
backup_folder = "backups"

def create_backup(filename):
    """
    Creates a timestamped backup copy of the target file in backups folder.
    """
    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_folder, f"{filename}_backup_{timestamp}")
    with open(filename, "r", encoding="utf-8") as original, \
         open(backup_path, "w", encoding="utf-8") as backup:
        backup.write(original.read())
    print(f"🛡️ Backup created: {backup_path}")

def parse_intent_line(intent_line):
    """
    Parses a single intent line string and returns a dict representing
    the action to take, including command, filename, line numbers, content.
    Raises ValueError if the intent line format is invalid.
    """
    patterns = {
        'modify': r"modify (\S+) at line (\d+) with (.+)",
        'insert': r"insert (\S+) at line (\d+) with (.+)",
        'delete': r"delete (\S+) from line (\d+) to (\d+)",
        'append': r"append (\S+) with (.+)",
        'replace': r"replace (\S+) lines (\d+)-(\d+) with (\[.*\])"
    }
    for command, pattern in patterns.items():
        match = re.match(pattern, intent_line)
        if match:
            if command in ['modify', 'insert']:
                filename, line_str, content = match.groups()
                return {
                    'command': command,
                    'filename': filename,
                    'line_start': int(line_str),
                    'line_end': None,
                    'content': content
                }
            elif command == 'delete':
                filename, start_str, end_str = match.groups()
                return {
                    'command': command,
                    'filename': filename,
                    'line_start': int(start_str),
                    'line_end': int(end_str),
                    'content': None
                }
            elif command == 'append':
                filename, content = match.groups()
                return {
                    'command': command,
                    'filename': filename,
                    'line_start': None,
                    'line_end': None,
                    'content': content
                }
            elif command == 'replace':
                filename, start_str, end_str, content_list_str = match.groups()
                content_list = ast.literal_eval(content_list_str)
                return {
                    'command': command,
                    'filename': filename,
                    'line_start': int(start_str),
                    'line_end': int(end_str),
                    'content': content_list
                }
    raise ValueError(f"Intent line format invalid or unsupported: {intent_line}")

def execute_intent(intent):
    """
    Executes the parsed intent on the target file.
    Creates a backup before applying changes.
    Includes safety checks for delete command to protect important code.
    """
    filename = intent['filename']
    abs_path = os.path.abspath(filename)
    print(f"🛠️ Attempting to modify file: {abs_path}")

    # Create backup before modifying
    create_backup(abs_path)

    with open(abs_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"📄 File '{filename}' currently has {len(lines)} lines.")

    command = intent['command']
    line_start = intent['line_start']
    line_end = intent['line_end']
    content = intent['content']

    if command == 'modify':
        if line_start < 1 or line_start > len(lines):
            raise IndexError(f"Line number {line_start} out of range in {filename}")
        lines[line_start - 1] = content + '\n'

    elif command == 'insert':
        if line_start < 1 or line_start > len(lines) + 1:
            raise IndexError(f"Line number {line_start} out of range for insert in {filename}")
        lines.insert(line_start - 1, content + '\n')

    elif command == 'delete':
        if line_start < 1 or line_end > len(lines) or line_start > line_end:
            raise IndexError(f"Invalid line range {line_start}-{line_end} for delete in {filename}")

        # Safety check: prevent deleting important lines
        unsafe = False
        for i in range(line_start - 1, line_end):
            line_content = lines[i].strip()
            if line_content.startswith('def ') or line_content.startswith('class ') or line_content == '':
                unsafe = True
                print(f"⚠️ Warning: Attempt to delete protected or blank line {i+1}: '{lines[i].rstrip()}'")

        if unsafe:
            print("❌ Delete aborted to protect important code.")
            return  # Skip deletion to keep file safe

        del lines[line_start - 1:line_end]

    elif command == 'append':
        lines.append(content + '\n')

    elif command == 'replace':
        if line_start < 1 or line_end > len(lines) or line_start > line_end:
            raise IndexError(f"Invalid line range {line_start}-{line_end} for replace in {filename}")
        if not isinstance(content, list):
            raise TypeError("Content for replace must be a list of lines")
        replacement = [line + '\n' for line in content]
        lines[line_start - 1:line_end] = replacement

    else:
        raise ValueError(f"Unsupported command: {command}")

    with open(abs_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Executed {command} on {abs_path} (lines {line_start}-{line_end if line_end else ''})")

def process_intents(intent_file=intent_file):
    """
    Reads the intent file, parses each intent line, and executes the intents.
    Orders execution to prevent line shifting issues.
    """
    print(f"🔍 Processing intents from {intent_file}...")

    try:
        with open(intent_file, "r", encoding="utf-8") as f:
            intent_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Intent file '{intent_file}' not found.")
        return

    if not intent_lines:
        print("⚠️ No intents found to process.")
        return

    intents = []
    for line in intent_lines:
        try:
            intent = parse_intent_line(line)
            intents.append(intent)
        except Exception as e:
            print(f"❌ Error parsing intent '{line}': {e}")

    # Commands that don't shift lines, executed top-down
    top_down_cmds = {'modify', 'replace', 'append'}
    # Commands that shift lines, executed bottom-up
    bottom_up_cmds = {'insert', 'delete'}

    # Sort top-down intents ascending by line number (None last)
    top_down_intents = sorted(
        (i for i in intents if i['command'] in top_down_cmds),
        key=lambda x: x['line_start'] if x['line_start'] is not None else float('inf')
    )

    # Sort bottom-up intents descending by line number
    bottom_up_intents = sorted(
        (i for i in intents if i['command'] in bottom_up_cmds),
        key=lambda x: x['line_start'] if x['line_start'] is not None else -1,
        reverse=True
    )

    # Execute top-down intents first
    for intent in top_down_intents:
        try:
            execute_intent(intent)
        except Exception as e:
            print(f"❌ Error executing intent: {e}")

    # Then execute bottom-up intents
    for intent in bottom_up_intents:
        try:
            execute_intent(intent)
        except Exception as e:
            print(f"❌ Error executing intent: {e}")

if __name__ == "__main__":
    process_intents()
