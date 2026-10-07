"""Shared helpers for generating gopherlings exercises."""
import json, os, pathlib

ROOT = pathlib.Path(__file__).parent
EX_DIR = ROOT / "exercises"
SOL_DIR = ROOT / "solutions"
PRISTINE_DIR = ROOT / ".pristine"

MANIFEST = []

def reset_dirs():
    pass  # dirs created per exercise; do not wipe blindly

def add_manifest(eid, edir, mode, hint, topic, expected=None):
    entry = {"id": eid, "dir": edir, "mode": mode, "hint": hint, "topic": topic}
    if expected is not None:
        entry["expectedOutput"] = expected
    MANIFEST.append(entry)

def write_files(edir, files):
    for base, content in files.items():
        for root in (EX_DIR / edir, SOL_DIR / edir, PRISTINE_DIR / edir):
            pass
    # exercise files (broken) -> EX_DIR + PRISTINE
    # solution files (fixed) -> SOL_DIR
    ex_files, sol_files, test_files = files["ex"], files["sol"], files.get("test")
    for d in (EX_DIR / edir, PRISTINE_DIR / edir):
        d.mkdir(parents=True, exist_ok=True)
        for name, content in ex_files.items():
            (d / name).write_text(content, encoding="utf-8", newline="\n")
        if test_files:
            for name, content in test_files.items():
                (d / name).write_text(content, encoding="utf-8", newline="\n")
    sdir = SOL_DIR / edir
    sdir.mkdir(parents=True, exist_ok=True)
    for name, content in sol_files.items():
        (sdir / name).write_text(content, encoding="utf-8", newline="\n")
    if test_files:
        for name, content in test_files.items():
            (sdir / name).write_text(content, encoding="utf-8", newline="\n")

def save_manifest():
    # sort by id
    MANIFEST.sort(key=lambda e: e["id"])
    (ROOT / "exercises.json").write_text(json.dumps(MANIFEST, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {len(MANIFEST)} entries to exercises.json")
