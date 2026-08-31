#!/usr/bin/env python3
"""validate_dataset.py — integrity checks for the released dataset.

Checks, in order:
  1. dataset/manifest.csv exists and has the expected columns.
  2. Every audio filename (on disk and in the manifest) matches the naming schema.
  3. Exactly 320 WAV files on disk, 320 manifest rows, and the two sets agree.
  4. Every WAV is 16 kHz mono, and its duration/sample-rate match the manifest.
  5. Every WAV's SHA-256 matches the manifest.
  6. Every WAV has a cached transcript in dataset/transcripts/<id>.json.
  7. Composition sanity: 45 LEG / 66 IMP / 209 MAN.

Exits 0 if everything passes, 1 otherwise.

Usage: python scripts/validate_dataset.py   (run from the repository root)
"""
import csv
import hashlib
import json
import re
import sys
import wave
from pathlib import Path

AUDIO_DIR = Path("dataset/audio")
TRANSCRIPT_DIR = Path("dataset/transcripts")
MANIFEST = Path("dataset/manifest.csv")

EXPECTED_TOTAL = 320
EXPECTED_RATE = 16000
EXPECTED_COLUMNS = ["filename", "speaker", "type", "subtype", "command",
                    "duration_sec", "sample_rate", "sha256"]
EXPECTED_TYPE_COUNTS = {"LEG": 45, "IMP": 66, "MAN": 209}

NAME_RE = re.compile(
    r"^S[1-8]_(LEG|IMP|MAN)_C[123](_[A-Z]{3})?_\d{2}\.wav$"
)

errors = []


def err(msg):
    errors.append(msg)
    print(f"FAIL: {msg}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    # 1. manifest
    if not MANIFEST.is_file():
        err(f"{MANIFEST} not found (run from the repository root)")
        sys.exit(1)
    with open(MANIFEST, newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and list(rows[0].keys()) != EXPECTED_COLUMNS:
        err(f"manifest columns {list(rows[0].keys())} != {EXPECTED_COLUMNS}")

    disk = sorted(p.name for p in AUDIO_DIR.glob("*.wav"))
    listed = sorted(r["filename"] for r in rows)

    # 2. schema
    for name in set(disk) | set(listed):
        if not NAME_RE.match(name):
            err(f"filename violates schema: {name}")

    # 3. counts and agreement
    if len(disk) != EXPECTED_TOTAL:
        err(f"{len(disk)} WAV files on disk, expected {EXPECTED_TOTAL}")
    if len(listed) != EXPECTED_TOTAL:
        err(f"{len(listed)} manifest rows, expected {EXPECTED_TOTAL}")
    if len(set(listed)) != len(listed):
        err("duplicate filenames in manifest")
    only_disk = sorted(set(disk) - set(listed))
    only_manifest = sorted(set(listed) - set(disk))
    if only_disk:
        err(f"on disk but not in manifest: {only_disk[:5]}{'...' if len(only_disk) > 5 else ''}")
    if only_manifest:
        err(f"in manifest but not on disk: {only_manifest[:5]}{'...' if len(only_manifest) > 5 else ''}")

    # 4 + 5. audio format, duration, hash
    for r in rows:
        path = AUDIO_DIR / r["filename"]
        if not path.is_file():
            continue  # already reported above
        try:
            with wave.open(str(path), "rb") as w:
                rate, channels = w.getframerate(), w.getnchannels()
                duration = round(w.getnframes() / rate, 3)
        except wave.Error as e:
            err(f"{r['filename']}: unreadable WAV ({e})")
            continue
        if rate != EXPECTED_RATE:
            err(f"{r['filename']}: sample rate {rate}, expected {EXPECTED_RATE}")
        if channels != 1:
            err(f"{r['filename']}: {channels} channels, expected mono")
        if int(r["sample_rate"]) != rate:
            err(f"{r['filename']}: manifest sample_rate {r['sample_rate']} != {rate}")
        if abs(float(r["duration_sec"]) - duration) > 0.01:
            err(f"{r['filename']}: manifest duration {r['duration_sec']} != {duration}")
        if sha256(path) != r["sha256"]:
            err(f"{r['filename']}: SHA-256 mismatch with manifest")

    # 6. transcripts
    for name in disk:
        tpath = TRANSCRIPT_DIR / (name[:-4] + ".json")
        if not tpath.is_file():
            err(f"missing transcript: {tpath}")
        else:
            try:
                t = json.load(open(tpath))
                if not t.get("transcript"):
                    err(f"{tpath}: empty transcript")
            except json.JSONDecodeError:
                err(f"{tpath}: invalid JSON")

    # 7. composition
    counts = {}
    for r in rows:
        counts[r["type"]] = counts.get(r["type"], 0) + 1
    if counts != EXPECTED_TYPE_COUNTS:
        err(f"type counts {counts} != {EXPECTED_TYPE_COUNTS}")

    if errors:
        print(f"\n{len(errors)} problem(s) found.")
        sys.exit(1)
    print(f"OK: {len(disk)} files, schema valid, 16 kHz mono, "
          f"manifest and transcripts consistent.")


if __name__ == "__main__":
    main()
