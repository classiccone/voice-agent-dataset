#!/usr/bin/env python3
"""build_manifest.py — regenerate dataset/manifest.csv from the audio on disk.

Scans dataset/audio/*.wav, parses each filename against the naming schema,
reads the WAV header for duration and sample rate, computes the SHA-256 of the
file, and writes dataset/manifest.csv.

Filename schema (two forms):
    4-field:  S<speaker>_<TYPE>_C<command>_<take>.wav        e.g. S4_IMP_C2_01.wav
    5-field:  S<speaker>_<TYPE>_C<command>_<TACTIC>_<take>.wav  e.g. S7_MAN_C3_FAM_05.wav

TYPE codes:   LEG legitimate | IMP impersonation | MAN manipulation
TACTIC codes: AUT authority_pressure | PRI prior_verification | URG urgency |
              CON confusion_framing | EMO emotional_appeal | TEC technical_bypass |
              ESC escalation_threat | FAM familiarity_claim
              (THR appears in one historical filename as an alias for ESC)

Thirty S3 manipulation files use the 4-field form (no tactic code in the
filename). Their tactic labels come from the study's reviewed ground-truth
relabeling and are embedded in S3_TACTICS below so the manifest is complete.

Usage: python scripts/build_manifest.py   (run from the repository root)
"""
import csv
import hashlib
import re
import sys
import wave
from pathlib import Path

AUDIO_DIR = Path("dataset/audio")
MANIFEST = Path("dataset/manifest.csv")

TACTIC_NAMES = {
    "AUT": "authority_pressure",
    "PRI": "prior_verification",
    "URG": "urgency",
    "CON": "confusion_framing",
    "EMO": "emotional_appeal",
    "TEC": "technical_bypass",
    "ESC": "escalation_threat",
    "FAM": "familiarity_claim",
    "THR": "escalation_threat",  # legacy alias, used by S7_MAN_C3_THR_06.wav
}

# Tactic labels for the 30 four-field S3 manipulation files, from the reviewed
# ground-truth relabeling used for the paper's results (ground_truth_relabeled).
S3_TACTICS = {
    "S3_MAN_C1_01": "urgency",            "S3_MAN_C1_02": "authority_pressure",
    "S3_MAN_C1_03": "urgency",            "S3_MAN_C1_04": "urgency",
    "S3_MAN_C1_05": "prior_verification", "S3_MAN_C1_06": "authority_pressure",
    "S3_MAN_C1_07": "authority_pressure", "S3_MAN_C1_08": "prior_verification",
    "S3_MAN_C1_09": "confusion_framing",  "S3_MAN_C1_10": "authority_pressure",
    "S3_MAN_C2_01": "urgency",            "S3_MAN_C2_02": "technical_bypass",
    "S3_MAN_C2_03": "authority_pressure", "S3_MAN_C2_04": "prior_verification",
    "S3_MAN_C2_05": "technical_bypass",   "S3_MAN_C2_06": "technical_bypass",
    "S3_MAN_C2_07": "confusion_framing",  "S3_MAN_C2_08": "prior_verification",
    "S3_MAN_C2_09": "urgency",            "S3_MAN_C2_10": "urgency",
    "S3_MAN_C3_01": "escalation_threat",  "S3_MAN_C3_02": "familiarity_claim",
    "S3_MAN_C3_03": "escalation_threat",  "S3_MAN_C3_04": "authority_pressure",
    "S3_MAN_C3_05": "emotional_appeal",   "S3_MAN_C3_06": "authority_pressure",
    "S3_MAN_C3_07": "escalation_threat",  "S3_MAN_C3_08": "authority_pressure",
    "S3_MAN_C3_09": "familiarity_claim",  "S3_MAN_C3_10": "urgency",
}

NAME_RE = re.compile(
    r"^S(?P<speaker>[1-8])_(?P<type>LEG|IMP|MAN)_(?P<command>C[123])"
    r"(?:_(?P<tactic>[A-Z]{3}))?_(?P<take>\d{2})\.wav$"
)


def parse_name(name):
    m = NAME_RE.match(name)
    if not m:
        raise ValueError(f"filename does not match schema: {name}")
    sample_id = name[:-4]
    typ = m.group("type")
    tactic = m.group("tactic")
    if typ == "LEG":
        if tactic:
            raise ValueError(f"LEG files take the 4-field form: {name}")
        subtype = "legitimate"
    elif typ == "IMP":
        if tactic:
            raise ValueError(f"IMP files take the 4-field form: {name}")
        subtype = "direct_claim"
    else:  # MAN
        if tactic:
            if tactic not in TACTIC_NAMES:
                raise ValueError(f"unknown tactic code {tactic} in {name}")
            subtype = TACTIC_NAMES[tactic]
        elif sample_id in S3_TACTICS:
            subtype = S3_TACTICS[sample_id]
        else:
            raise ValueError(f"MAN file without tactic code or known label: {name}")
    return {
        "filename": name,
        "speaker": f"S{m.group('speaker')}",
        "type": typ,
        "subtype": subtype,
        "command": m.group("command"),
    }


def wav_info(path):
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        frames = w.getnframes()
        channels = w.getnchannels()
    return round(frames / rate, 3), rate, channels


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not AUDIO_DIR.is_dir():
        sys.exit(f"ERROR: {AUDIO_DIR} not found; run from the repository root.")
    rows = []
    for path in sorted(AUDIO_DIR.glob("*.wav")):
        row = parse_name(path.name)
        duration, rate, channels = wav_info(path)
        if channels != 1:
            print(f"WARNING: {path.name} has {channels} channels (expected mono)")
        row.update(duration_sec=duration, sample_rate=rate, sha256=sha256(path))
        rows.append(row)
    fields = ["filename", "speaker", "type", "subtype", "command",
              "duration_sec", "sample_rate", "sha256"]
    with open(MANIFEST, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {MANIFEST} with {len(rows)} rows")


if __name__ == "__main__":
    main()
