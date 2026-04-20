#! /Users/yeshwanth/.venv/bin/python
# read markdown front matter and print it
"""EG
import frontmatter

input = '''
---
title: My Cats
categories: ["cats","pets"]
description: Why cats are better than dogs.
---

This is the rest of the content.
'''

data = frontmatter.loads(input)

print("Title", data["title"])
print("Categories", data["categories"])
print("Description", data["description"])

print("Content", data.content)
"""
import os
from pathlib import Path
import frontmatter

def _print_front_matter(input_path, keyword=None):
    # if directory, find all .md files and print their front matter
    if os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    print_front_matter(file_path, keyword)
    else:
        truncated_path = f'.../{Path(input_path).parent.parent.name}/{Path(input_path).parent.name}/{Path(input_path).name}'
        with open(input_path, 'r') as f:
            data = frontmatter.load(f)
        if not data.metadata:
            return
        # print path up to two parents only
        if keyword:
            # if keyword is provided print all kv pairs if even one of the key or value contains the keyword (case-insensitive)
            if any(keyword.lower() in str(key).lower() or keyword.lower() in str(value).lower() for key, value in data.metadata.items()):
                return print(f"{truncated_path}:\n" + "\n".join([f"{key}: {value}" for key, value in data.metadata.items()]), end="\n---\n")
            elif keyword.lower() in truncated_path.lower():
                return print(f"{truncated_path}:\n" + "\n".join([f"{key}: {value}" for key, value in data.metadata.items()]), end="\n---\n")
        else:
            return print("\n".join([f"{key}: {value}" for key, value in data.metadata.items()]), end="\n---\n")

def print_front_matter(input_path, keyword=None):
    try:
        _print_front_matter(input_path, keyword)
    except Exception as e:
        import traceback
        print(f"Error reading {input_path}: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Read markdown front matter and print it')
    parser.add_argument('input_path', type=str, help='Path to the markdown file')
    parser.add_argument('--keyword', type=str, help='Keyword to search for in the front matter')
    args = parser.parse_args()

    print_front_matter(args.input_path, args.keyword)