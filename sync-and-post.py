import subprocess
import sys
import os

# Verify we're in the project folder
if not os.path.exists("quartz.config.ts"):
    print("Error: quartz.config.ts not found. Run this script from the project root.", file=sys.stderr)
    sys.exit(1)

result = subprocess.run(["python3", "sync-with-vault.py"])
if result.returncode != 0:
    sys.exit(1)

subprocess.run(["npx", "quartz", "sync"], check=True)
