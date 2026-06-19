#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Move Bible JSON files into territory folders and rename them.

Example:
    France - Bible J.N. Darby.json

Becomes:
    France/Bible J.N. Darby.json

How to use:
1. Put this script inside the folder that contains all your .json Bible files.
2. Run:
       python move_json_to_territory_folders.py

It only processes JSON files that contain:
       Territory - Bible Title.json

It will skip files that do not contain " - " in the filename.
"""

import shutil
from pathlib import Path


SCRIPT_NAME = Path(__file__).name


def safe_name(name: str) -> str:
    """
    Clean names for Windows folders/files.
    """
    bad_chars = '<>:"/\\|?*'
    for ch in bad_chars:
        name = name.replace(ch, " ")
    name = " ".join(name.split()).strip()
    return name


def unique_path(path: Path) -> Path:
    """
    If a file already exists, create a safe numbered name:
    Bible.json
    Bible (2).json
    Bible (3).json
    """
    if not path.exists():
        return path

    parent = path.parent
    stem = path.stem
    suffix = path.suffix

    counter = 2
    while True:
        new_path = parent / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def main():
    current_dir = Path.cwd()

    json_files = [
        p for p in current_dir.glob("*.json")
        if p.is_file()
    ]

    if not json_files:
        print("No JSON files found in this folder.")
        print("Put this script in the folder that contains your converted Bible JSON files.")
        return

    moved = 0
    skipped = 0

    print(f"Found {len(json_files)} JSON file(s).")
    print()

    for json_file in sorted(json_files):
        filename = json_file.stem

        if " - " not in filename:
            print(f"SKIPPED: {json_file.name}")
            print("         Filename does not contain ' - '")
            skipped += 1
            continue

        territory, bible_title = filename.split(" - ", 1)

        territory = safe_name(territory)
        bible_title = safe_name(bible_title)

        if not territory or not bible_title:
            print(f"SKIPPED: {json_file.name}")
            print("         Territory or Bible title is empty after cleaning.")
            skipped += 1
            continue

        territory_folder = current_dir / territory
        territory_folder.mkdir(exist_ok=True)

        destination = territory_folder / f"{bible_title}.json"
        destination = unique_path(destination)

        try:
            shutil.move(str(json_file), str(destination))
            print(f"OK: {json_file.name}")
            print(f"    Moved to: {destination.relative_to(current_dir)}")
            moved += 1
        except Exception as e:
            print(f"ERROR: {json_file.name}")
            print(f"       {e}")
            skipped += 1

    print()
    print("Done.")
    print(f"Moved: {moved}")
    print(f"Skipped/Failed: {skipped}")


if __name__ == "__main__":
    main()
