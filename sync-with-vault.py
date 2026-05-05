import os
import re
import shutil
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Obsidian image embed patterns ![[image.png]]
IMAGE_PATTERNS = [
    re.compile(r"!\[\[(?=[^]]*\.)[^]]+?\]\]"),
]

# Please change these to your use case.
DEFAULT_VAULT_DIR = "~/diamond"
DEFAULT_QUARTZ_DIR = "./content"


# Helper function to extract images from markdown content
def extract_images(markdown_text):
    images = set()
    for pattern in IMAGE_PATTERNS:
        for match in pattern.findall(markdown_text):
            images.add(match.split("|")[0])  # remove Obsidian alias if present
    logging.info(f"Found images: {images}")
    return images


# Helper function to check if 'publish' is in tags
def has_publish_tag(front_matter):
    # 1. Single-line tags: tags: [publish, crypto]
    single_line = re.search(r"^tags:\s*\[([^\]]*)\]", front_matter, re.MULTILINE)
    if single_line:
        tags_list = [tag.strip() for tag in single_line.group(1).split(",")]
        logging.debug(f"Single-line tags found: {tags_list}")
        if "publish" in tags_list:
            return True

    # 2. Multi-line tags:
    # tags:
    #   - publish
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


# Helper function to copy files preserving folder structure
def copy_file(src_path, dst_root, root_dir, inject_publish=False):
    rel_path = os.path.relpath(src_path, root_dir)
    out_path = os.path.join(dst_root, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if inject_publish and src_path.lower().endswith(".md"):
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Add publish: true to existing frontmatter
        content = re.sub(
            r"^(---\n)(.*?)(^---)",
            r"\1\2publish: true\n\3",
            content,
            count=1,
            flags=re.DOTALL | re.MULTILINE,
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Copied (with publish property) '{src_path}' to '{out_path}'")
    else:
        shutil.copy2(src_path, out_path)
        logging.info(f"Copied '{src_path}' to '{out_path}'")
    return out_path


def main(src, dst):
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)
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

            # Extract YAML front matter
            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not match:
                logging.info(f"No front matter found in '{md_path}', skipping.")
                continue  # skip if no front matter

            front_matter = match.group(1)

            # Only include if 'publish' is in tags
            if not has_publish_tag(front_matter):
                logging.info(f"'publish' tag not found in '{md_path}', skipping.")
                continue

            # copy markdown file, injecting publish: true property
            copy_file(md_path, dst, src, inject_publish=True)

            # copy linked images
            for img in extract_images(content):
                img_path = os.path.join(root, img)
                if os.path.isfile(img_path):
                    copy_file(img_path, dst, src)
                else:
                    logging.warning(f"Image not found: {img_path}")


if __name__ == "__main__":
    main(DEFAULT_VAULT_DIR, DEFAULT_QUARTZ_DIR)
