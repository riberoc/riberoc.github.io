import subprocess
import sys
import os

# Verify we're in the project folder. Quartz v5 projects use quartz.config.yaml
# together with quartz.ts; older projects may use quartz.config.ts.
project_files = ("quartz.config.yaml", "quartz.config.ts", "quartz.ts")
if not any(os.path.exists(filename) for filename in project_files):
    print(
        "Error: Quartz project configuration not found. "
        "Run this script from the project root.",
        file=sys.stderr,
    )
    sys.exit(1)

result = subprocess.run([sys.executable, "sync-with-vault.py"])
if result.returncode != 0:
    sys.exit(1)

subprocess.run(["npm", "run", "quartz", "--", "sync"], check=True)
