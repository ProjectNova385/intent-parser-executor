# Intent Parser Executor

A lightweight and flexible Python framework for **parsing**, **validating**, and **executing** file modification instructions (intents).  
Perfect for automating structured file edits with safety features like backups and protected code checks.

---

## ✨ Features

- **Structured Intent Parsing** – Supports `modify`, `insert`, `delete`, `append`, and `replace` commands.
- **Backup Creation** – Automatically creates timestamped backups before modifying files.
- **Safety Checks** – Prevents accidental deletion of critical code (e.g., `def`, `class` definitions).
- **Execution Order Control** – Processes commands in the correct order to prevent line shifting errors.
- **Extensible** – Easy to adapt for different project needs.

---

## 📂 Project Structure

intent-parser-executor/
├── backups/ # Auto-generated backups folder
├── LICENSE # MIT License
├── intent-parser-executor_intents.txt # Intent instructions file
└── intent_manager.py # Main framework script



---

## 📜 Intent File Format

Each line in the `intent-parser-executor_intents.txt` file should be a single command in the supported format:

**Supported Commands:**
modify filename at line X with new_content
insert filename at line X with new_content
delete filename from line X to Y
append filename with new_content
replace filename lines X-Y with ["line1", "line2", ...]



---

**Examples:**
modify example.py at line 10 with print("Hello, World!")
insert example.py at line 5 with import os
delete example.py from line 20 to 25
append example.py with # End of script
replace example.py lines 30-32 with ["print('Line 1')", "print('Line 2')"]


---

## 🚀 Usage

1. **Place your intent commands** in `intent-parser-executor_intents.txt`
2. **Run the framework**:
   ```bash
   python intent_manager.py
Check the console logs for operation results

Review backups in the backups/ folder if needed

🛡️ Safety Notes
Backups are stored in /backups with timestamps before each file change.

Delete Protection: Will not remove def, class, or empty lines to prevent breaking code.

Absolute Paths: Framework works with relative or absolute file paths.

⚙️ Customization
To adapt for your project:

Open intent_manager.py

Search for your_project_title_here and replace it with your actual project name (already set to intent-parser-executor here).

Update intent_file variable to point to your .txt file with intents.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

💡 Pro Tip: Use CTRL+F in your code editor to search for intent-parser-executor and update any other references as needed.

