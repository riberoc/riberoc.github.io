import os

# Sequential, generic names ordered in a logical web navigation flow
GENERIC_FLOW = [
    "index",
    "home",
    "welcome",
    "main",
    "overview",
    "dashboard",
    "summary",
    "details",
    "info",
    "content",
]


def generate_redirect_chain(count: int, output_dir: str):
    """Generates `count` HTML files linked in a logical sequential flow."""
    os.makedirs(output_dir, exist_ok=True)

    # Build sequence using logical flow names, falling back to page-N if needed
    filenames = []
    for i in range(count):
        if i < len(GENERIC_FLOW):
            name = GENERIC_FLOW[i]
        else:
            name = f"page-{i + 1}"
        filenames.append(f"{name}.html")

    # Write each file pointing to the next logical step in the chain
    for i in range(count):
        current_file = filenames[i]
        # The last file points to a logical destination like landing.html
        next_file = filenames[i + 1] if i + 1 < count else "landing.html"

        content = f"""302 nginx
302 Moved
302 Moved to `{next_file}` - fetch next.
"""

        file_path = os.path.join(output_dir, current_file)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Created: {file_path} -> Points to {next_file}")


if __name__ == "__main__":
    # Settings
    NUMBER_OF_FILES = 5
    OUTPUT_DIRECTORY = ".."

    generate_redirect_chain(NUMBER_OF_FILES, OUTPUT_DIRECTORY)
