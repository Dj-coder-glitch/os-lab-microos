#!/usr/bin/env python3
"""
Uploads the OS project to Hugging Face Dataset: vedraj1309/oslab
"""

import sys, os
from huggingface_hub import HfApi

TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HF_TOKEN")
if not TOKEN:
    print("Error: No HF_TOKEN provided")
    sys.exit(1)

REPO_ID = "vedraj1309/oslab"
FOLDER = r"c:\Users\prath\OneDrive\Documents\OS mini project"

print(f"Connecting to Hugging Face repository {REPO_ID}...")
api = HfApi(token=TOKEN)

user_info = api.whoami()
username = user_info.get("name") or user_info.get("fullname") or "vedraj1309"
print(f"Authenticated as: {username}")

# Prepend dataset card frontmatter to README if not present
readme_path = os.path.join(FOLDER, "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

if not readme_content.startswith("---"):
    frontmatter = """---
annotations_creators: []
language:
- en
license: mit
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets: []
task_categories:
- other
task_ids: []
pretty_name: "Aurora Neural OS v2.6 // x86_64 Rust Microkernel"
tags:
- operating-system
- rust
- microkernel
- x86_64
- page-replacement
- os-lab
---

"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + readme_content)
    print("Added dataset YAML metadata card to README.md")

print("Uploading files to Hugging Face dataset...")
res = api.upload_folder(
    folder_path=FOLDER,
    repo_id=REPO_ID,
    repo_type="dataset",
    ignore_patterns=[
        "*.vdi",
        "*.vmdk",
        "*.nvram",
        "target/**",
        "**/target/**",
        "vm_*.png",
        "term_*.png",
        "*.log",
        ".git/**",
        "__pycache__/**",
        "*.pyc",
        ".idea/**",
        ".vscode/**",
        "scripts/push_to_huggingface.py",
    ],
    commit_message="feat: Aurora Neural OS v2.6 x86_64 microkernel, white theme GUI, and page replacement research",
)

print("Upload successful!")
print("Commit URL:", res)
