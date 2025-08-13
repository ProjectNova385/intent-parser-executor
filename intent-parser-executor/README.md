# Intent Parsing and Execution Framework

Easily define code changes in a text file and let Python handle the rest.  
This framework automates inserts, deletes, replaces, and more—backed up and safe.

---

## Features

- **Modify lines**: Change existing lines in your code.
- **Insert lines**: Add new lines at specific locations.
- **Delete lines**: Remove lines safely with protections for important code.
- **Append lines**: Add lines at the end of files.
- **Replace lines**: Replace multiple lines at once.
- **Automatic backups**: Every file modification is backed up with a timestamp.
- **Safety checks**: Prevents accidental deletion of functions, classes, or blank lines.

---

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Intent-Parsing-and-Execution-Framework.git

2. Navigate to the project folder:
cd Intent-Parsing-and-Execution-Framework

3. Install any dependencies (if required):
pip install -r requirements.txt

4. Define your intents in project_title_intents.txt (formerly nova_intents.txt):

Examples of intents:

insert your_file.py at line 6 with print("🔥 Inserted line!")

delete your_file.py from line 3 to 4

replace your_file.py lines 10-11 with ["print('🔥 line 10 replaced')", "print('🔥 line 11 replaced')"]

Run the intent manager:
python project_title_intent_manager.py

HOW IT WORKS
The manager reads each intent from the intents file.

Executes commands safely while creating backups.

Handles line shifts correctly by sorting inserts/deletes and replacements/modifications in the right order

NOTES
Replace all instances of your_project_title_here with your actual project name in comments and filenames.

Backups are saved in the backups folder with timestamps
