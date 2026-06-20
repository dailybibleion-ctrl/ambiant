import re
from pathlib import Path

# ============================================================
# Rename English Bible JSON files to full Bible version names
# ============================================================
# Put this script in the folder that contains your "English" folder,
# then run:
#
#   python rename_english_json_full_names.py
#
# It will rename:
#   KJV.json  -> King James Version.json
#   WEB.json  -> World English Bible.json
#   BSB.json  -> Berean Standard Bible.json
#
# If the "English" folder is not found, it will rename JSON files
# in the current folder.
# ============================================================

TARGET_FOLDER = Path("English")

if not TARGET_FOLDER.exists():
    TARGET_FOLDER = Path(".")

# Add or edit names here if needed.
FULL_NAME_MAP = {
    "KJV": "King James Version",
    "AKJV": "American King James Version",
    "KJVA": "King James Version with Apocrypha",
    "KJVAE": "King James Version with Apocrypha",
    "KJV STRONGS": "King James Version Strongs",
    "KJV_STRONGS": "King James Version Strongs",

    "WEB": "World English Bible",
    "WEBBE": "World English Bible British Edition",
    "WEBA": "World English Bible with Apocrypha",
    "WEBUS": "World English Bible American English Edition",

    "BSB": "Berean Standard Bible",
    "ASV": "American Standard Version",
    "ASVBT": "American Standard Version Byzantine Text",
    "BBE": "Bible in Basic English",
    "DARBY": "Darby Bible Translation",
    "DRC": "Douay Rheims Challoner Revision",
    "DRA": "Douay Rheims American Edition",
    "ERV": "English Revised Version",
    "GNV": "Geneva Bible",
    "JUB": "Jubilee Bible",
    "LEB": "Lexham English Bible",
    "LSV": "Literal Standard Version",
    "NET": "New English Translation",
    "NHEB": "New Heart English Bible",
    "NHEBJE": "New Heart English Bible Jehovah Edition",
    "NHEBME": "New Heart English Bible Messianic Edition",
    "NHEB YHWH": "New Heart English Bible YHWH Edition",
    "NHEB_YHWH": "New Heart English Bible YHWH Edition",
    "OEB": "Open English Bible",
    "OEBUS": "Open English Bible US Edition",
    "T4T": "Translation for Translators",
    "TFT": "Translation for Translators",
    "WBT": "Webster Bible Translation",
    "WYC": "Wycliffe Bible",
    "YLT": "Youngs Literal Translation",

    "NKJV": "New King James Version",
    "ESV": "English Standard Version",
    "NIV": "New International Version",
    "NRSV": "New Revised Standard Version",
    "NRSVUE": "New Revised Standard Version Updated Edition",
    "CSB": "Christian Standard Bible",
    "NASB": "New American Standard Bible",
    "NASB1995": "New American Standard Bible 1995",
    "NASB95": "New American Standard Bible 1995",
    "NLT": "New Living Translation",
    "NLV": "New Life Version",
    "AMP": "Amplified Bible",
    "AMPC": "Amplified Bible Classic Edition",
    "CEV": "Contemporary English Version",
    "CEB": "Common English Bible",
    "GNT": "Good News Translation",
    "GW": "Gods Word Translation",
    "HCSB": "Holman Christian Standard Bible",
    "ICB": "International Childrens Bible",
    "ISV": "International Standard Version",
    "MSG": "The Message",
    "NABRE": "New American Bible Revised Edition",
    "NCV": "New Century Version",
    "NIRV": "New International Readers Version",
    "RSV": "Revised Standard Version",
    "TLB": "The Living Bible",
    "VOICE": "The Voice",

    "BISHOP": "Bishops Bible",
    "BISHOPS": "Bishops Bible",
    "COVERDALE": "Coverdale Bible",
    "TYNDALE": "Tyndale Bible",
    "WESLEY": "Wesley Bible",
    "RVB": "Revised Version Bible",
}

INVALID_WINDOWS_CHARS = r'<>:"/\|?*'


def safe_filename(name):
    for ch in INVALID_WINDOWS_CHARS:
        name = name.replace(ch, "")
    name = re.sub(r"\s+", " ", name).strip()
    return name


def normalize_key(name):
    key = Path(name).stem
    key = key.replace("_", " ")
    key = key.replace("-", " ")
    key = re.sub(r"\s+", " ", key).strip()
    return key.upper()


def make_unique_path(path):
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2

    while True:
        new_path = parent / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def main():
    json_files = [
        p for p in TARGET_FOLDER.glob("*.json")
        if p.is_file() and not p.name.startswith("_")
    ]

    if not json_files:
        print(f"No JSON files found in: {TARGET_FOLDER.resolve()}")
        return

    print(f"Renaming JSON files in: {TARGET_FOLDER.resolve()}")
    print(f"Found {len(json_files)} JSON files.")
    print()

    renamed = 0
    skipped = 0

    skipped_files = []

    for path in sorted(json_files):
        key = normalize_key(path.name)

        full_name = FULL_NAME_MAP.get(key)

        if not full_name:
            skipped += 1
            skipped_files.append(path.name)
            print(f"SKIPPED: {path.name}  -> no full name found")
            continue

        new_name = safe_filename(full_name) + ".json"
        new_path = path.with_name(new_name)

        if path.name == new_name:
            print(f"OK already named: {path.name}")
            continue

        final_path = make_unique_path(new_path)
        path.rename(final_path)

        renamed += 1
        print(f"RENAMED: {path.name}  ->  {final_path.name}")

    print()
    print("Done.")
    print(f"Renamed: {renamed}")
    print(f"Skipped: {skipped}")

    if skipped_files:
        skipped_txt = TARGET_FOLDER / "_skipped_unknown_names.txt"
        skipped_txt.write_text("\n".join(skipped_files), encoding="utf-8")
        print()
        print(f"Unknown/skipped names saved to: {skipped_txt.resolve()}")
        print("Add those abbreviations to FULL_NAME_MAP in the script, then run it again.")


if __name__ == "__main__":
    main()
