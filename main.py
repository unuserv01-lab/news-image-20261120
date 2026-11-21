"""news-image-20261120 entry: copy the front-page image to /output/entry.png.

The image is the front page of THE WORLD LEDGER for Friday 20 November
2026, built at build time (render.py renders stories.json to entry.png).
This program deterministically copies it to the grader's output directory.
It runs with no network, in a read-only container, and writes identical
bytes on every run.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)

# The gate requires both runs to write the same bytes; a plain copy of a
# fixed file is deterministic by construction, and we assert the copy
# landed with the exact size of the source.
assert os.path.getsize(OUT) == os.path.getsize(SRC), "copy size mismatch"
