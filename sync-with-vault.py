import os
import shutil
import re
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Obsidian wikilink/embed patterns: ![[file.ext]] and [[file.ext]]
WIKILINK_PATTERNS = [
    re.compile(r"!?\[\[(?=[^]]*\.)[^]]+?\]\]"),
]

# Standard markdown link pattern: [text](file.ext)
MDLINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+\.[^)]+)\)")

# Please change these to your use case.
DEFAULT_VAULT_DIR = "~/diamond"
DEFAULT_QUARTZ_DIR = "./content"


def clean_frontmatter_links(front_matter):
    def replace_cover(match):
        value = match.group(1).strip()
        # ONLY remove quotes (nothing else)
        value = value.strip('"').strip("'")
        return f"cover: {value}"

    front_matter = re.sub(
        r"^cover:\s*(.+)$", replace_cover, front_matter, flags=re.MULTILINE
    )
    return front_matter


def extract_assets(markdown_text):
    assets = set()
    for pattern in WIKILINK_PATTERNS:
        for match in pattern.findall(markdown_text):
            inner = re.sub(r"^!?\[\[|\]\]$", "", match)
            assets.add(inner.split("|")[0].strip())
    for match in MDLINK_PATTERN.findall(markdown_text):
        if not match.startswith("http") and not match.startswith("#"):
            assets.add(match.strip())
    logging.info(f"Found assets: {assets}")
    return assets


def find_in_vault(filename, vault_root):
    """Search entire vault for a file by basename."""
    basename = os.path.basename(filename)
    for root, _, files in os.walk(vault_root):
        if basename in files:
            return os.path.join(root, basename)
    return None


def has_publish_tag(front_matter):
    # 1. Single-line tags: tags: [publish, crypto]
    single_line = re.search(r"^tags:\s*\[([^\]]*)\]", front_matter, re.MULTILINE)
    if single_line:
        tags_list = [tag.strip() for tag in single_line.group(1).split(",")]
        logging.debug(f"Single-line tags found: {tags_list}")
        if "publish" in tags_list:
            return True

    # 2. Multi-line tags
    multi_line = re.search(
        r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", front_matter, re.MULTILINE
    )
    if multi_line:
        tags_list = [
            line.strip()[2:].strip() for line in multi_line.group(1).splitlines()
        ]
        logging.debug(f"Multi-line tags found: {tags_list}")
        if "publish" in tags_list:
            return True

    return False


def copy_asset_file(src_path, dst_root, root_dir):
    """Copies static asset files directly."""
    rel_path = os.path.relpath(src_path, root_dir)
    out_path = os.path.join(dst_root, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    shutil.copy2(src_path, out_path)
    logging.info(f"Copied asset '{src_path}' to '{out_path}'")
    return out_path


def write_modified_md(content, src_path, dst_root, root_dir):
    """Writes the updated in-memory markdown content to the destination."""
    rel_path = os.path.relpath(src_path, root_dir)
    out_path = os.path.join(dst_root, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Inject publish: true to the frontmatter string
    content = re.sub(
        r"^(---\n)(.*?)(^---)",
        r"\1\2publish: true\n\3",
        content,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(
        f"Saved processed MD (with quotes stripped & publish tag) to '{out_path}'"
    )
    return out_path


def main(src, dst):
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)

    if os.path.exists(dst):
        shutil.rmtree(dst)
        logging.info(f"Cleaned destination folder: {dst}")

    os.makedirs(dst, exist_ok=True)
    logging.info(f"Starting copy from '{src}' to '{dst}'")

    for root, _, files in os.walk(src):
        for file in files:
            if not file.lower().endswith(".md"):
                continue

            md_path = os.path.join(root, file)
            logging.info(f"Processing markdown file: {md_path}")

            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not match:
                logging.info(f"No front matter found in '{md_path}', skipping.")
                continue

            raw_front = match.group(1)
            front_matter = clean_frontmatter_links(raw_front)

            # Replace the old front matter with the cleaned one in our content string
            content = content.replace(raw_front, front_matter)

            # Check if 'publish' is in tags using the updated front_matter
            if not has_publish_tag(front_matter):
                logging.info(f"'publish' tag not found in '{md_path}', skipping.")
                continue

            # Process the cover asset if it exists
            cover_match = re.search(r"^cover:\s*(.+)$", front_matter, re.MULTILINE)
            if cover_match:
                cover = cover_match.group(1).strip().strip('"').strip("'")
                logging.info(f"Found cover: {cover}")

                if not cover.startswith("http"):
                    asset = cover
                    local_path = os.path.join(root, os.path.basename(asset))
                    if os.path.isfile(local_path):
                        copy_asset_file(local_path, dst, src)
                    else:
                        found = find_in_vault(asset, src)
                        if found:
                            copy_asset_file(found, dst, src)
                        else:
                            logging.warning(f"Cover not found: {asset}")

            # Save the modified markdown file to destination
            write_modified_md(content, md_path, dst, src)

            # Copy other linked assets
            for asset in extract_assets(content):
                local_path = os.path.join(root, os.path.basename(asset))
                if os.path.isfile(local_path):
                    copy_asset_file(local_path, dst, src)
                else:
                    found = find_in_vault(asset, src)
                    if found:
                        copy_asset_file(found, dst, src)
                    else:
                        logging.warning(f"Asset not found: {asset}")


if __name__ == "__main__":
    main(DEFAULT_VAULT_DIR, DEFAULT_QUARTZ_DIR)
