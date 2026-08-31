#!/usr/bin/env python3
"""transcribe.py — regenerate the cached Whisper transcripts from the audio.

Transcribes every WAV in dataset/audio/ with local Whisper (base model, the
snapshot used for the paper) and writes dataset/transcripts/<sample_id>.json
in the cached format:

    {"transcript": "<text>", "stt_time_ms": <int>}

The released transcripts were produced once and then cached, so every guardrail
level in the evaluation scores the exact same text. Re-running this script may
produce slightly different text on different Whisper builds/hardware; to
reproduce the paper's numbers, use the released transcripts as-is.

Requires: pip install openai-whisper   (https://github.com/openai/whisper)

Usage:
    python scripts/transcribe.py             # skip files that already have transcripts
    python scripts/transcribe.py --force     # re-transcribe everything
"""
import argparse
import json
import time
from pathlib import Path

AUDIO_DIR = Path("dataset/audio")
TRANSCRIPT_DIR = Path("dataset/transcripts")
WHISPER_MODEL = "base"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-transcribe files that already have a transcript")
    args = ap.parse_args()

    import whisper  # deferred so --help works without the dependency
    model = whisper.load_model(WHISPER_MODEL)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    wavs = sorted(AUDIO_DIR.glob("*.wav"))
    done = 0
    for path in wavs:
        out = TRANSCRIPT_DIR / (path.stem + ".json")
        if out.exists() and not args.force:
            continue
        t0 = time.time()
        result = model.transcribe(str(path), language="en")
        elapsed_ms = round((time.time() - t0) * 1000)
        out.write_text(json.dumps(
            {"transcript": result["text"].strip(), "stt_time_ms": elapsed_ms},
            indent=2))
        done += 1
        print(f"[{done}] {path.name} -> {out.name}")
    print(f"transcribed {done} of {len(wavs)} files "
          f"({len(wavs) - done} already cached)")


if __name__ == "__main__":
    main()
