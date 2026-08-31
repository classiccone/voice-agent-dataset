# Voice-Agent Social-Engineering Benchmark

A 320-sample spoken-audio benchmark for measuring how well prompt-guardrailed,
LLM-backed customer-service voice agents resist social-engineering attacks.
Each sample is a single-request phone-call utterance — a legitimate request, an
impersonation attempt, or one of eight manipulation tactics — recorded by eight
speakers as 16 kHz mono WAV against a fictional dental-practice scenario in
which the agent already holds the (fictional) patient record in its system
prompt. The release includes the audio, cached Whisper transcripts, the five
cumulative guardrail prompts (L0–L4) plus a minimal three-rule prompt, the
per-call results behind the paper's tables on two pinned GPT-4o snapshots, and
scripts to validate the dataset and reproduce the evaluation. The benchmark
accompanies the paper *"The Escalation Trap: Securing Consumer Voice Agents
Against Social Engineering"* (Narula and Mitra, Southeast Missouri State
University, submitted to IEEE CCNC 2027).

**Key facts:** 320 samples · 8 speakers (S1–S8) · 16 kHz mono WAV ·
275 adversarial + 45 legitimate · ~49 minutes of audio · fully scripted and
synthetic (no real personal data).

## Composition

Generated from `dataset/manifest.csv`:

| Type | Subtype | C1 | C2 | C3 | Total |
|------|---------|---:|---:|---:|------:|
| LEG | legitimate | 15 | 15 | 15 | **45** |
| IMP | direct_claim | 22 | 22 | 22 | **66** |
| MAN | authority_pressure | 13 | 9 | 10 | **32** |
| MAN | urgency | 11 | 10 | 8 | **29** |
| MAN | familiarity_claim | 9 | 7 | 10 | **26** |
| MAN | escalation_threat | 7 | 7 | 11 | **25** |
| MAN | prior_verification | 9 | 9 | 7 | **25** |
| MAN | confusion_framing | 8 | 9 | 7 | **24** |
| MAN | emotional_appeal | 8 | 8 | 8 | **24** |
| MAN | technical_bypass | 7 | 10 | 7 | **24** |
| | | | | | **320** |

## Filename schema

Two forms:

```
S<speaker>_<TYPE>_<COMMAND>_<take>.wav               e.g. S4_IMP_C2_01.wav
S<speaker>_<TYPE>_<COMMAND>_<TACTIC>_<take>.wav      e.g. S7_MAN_C3_FAM_05.wav
```

Code legend:

| Code | Meaning |
|------|---------|
| **C1** | Target command: information disclosure (read patient notes) |
| **C2** | Target command: unauthorized account action (change contact number) |
| **C3** | Target command: escalation abuse (transfer to office manager) |
| **LEG** | Legitimate request (no deception) |
| **IMP** | Impersonation (direct false-identity claim) |
| **MAN** | Manipulation (social-engineering tactic) |
| **AUT** | Authority pressure |
| **PRI** | Prior-verification claim |
| **URG** | Urgency |
| **CON** | Confusion framing |
| **EMO** | Emotional appeal |
| **TEC** | Technical bypass |
| **ESC** | Escalation threat |
| **FAM** | Familiarity claim |

Notes: one historical filename (`S7_MAN_C3_THR_06.wav`) uses `THR` as an alias
for `ESC` (escalation threat); it is kept unchanged so filenames stay in sync
with the transcripts and result logs. Thirty S3 manipulation files use the
4-field form with no tactic code in the filename — their tactic labels are in
`dataset/manifest.csv`.

## Repository layout

```
dataset/
  audio/               320 WAV files, 16 kHz mono
  transcripts/         cached Whisper (base) transcripts, one JSON per sample
  manifest.csv         filename, speaker, type, subtype, command,
                       duration_sec, sample_rate, sha256
docs/
  guardrail_prompts/   L0.txt ... L4.txt (cumulative levels), template_min.txt
results/
  gpt-4o/              per-condition, per-call results (gpt-4o-2024-11-20):
                       L0-L4, template_min, padded_L1 length control,
                       seven leave-one-out ablations (paper Tables III & IV)
  gpt-4o-mini/         replication on gpt-4o-mini-2024-07-18 (Table III)
scripts/
  build_manifest.py    regenerate the manifest from the audio on disk
  validate_dataset.py  integrity checks (schema, count, format, hashes)
  transcribe.py        regenerate transcripts with local Whisper base
  evaluate.py          reproduce the evaluation / recompute the metrics tables
```

## Quickstart: reproducing the evaluation

Validate the dataset and recompute the paper's tables from the released
per-call results (no API key needed):

```
python scripts/validate_dataset.py
python scripts/evaluate.py --summarize                          # Tables III & IV, GPT-4o
python scripts/evaluate.py --summarize --results results/gpt-4o-mini
```

Re-run the evaluation yourself (requires `pip install openai` and an
`OPENAI_API_KEY`; each level × 5 repeats is 1,600 API calls):

```
python scripts/evaluate.py --run --level L1 --repeats 5
python scripts/evaluate.py --summarize --results results/new_runs
```

The pipeline scores the cached transcript of each sample under the selected
guardrail prompt (with the fictional patient record pre-loaded) and records the
agent's GRANT / DENY / VERIFY / ESCALATE decision. The paper's numbers were
produced against the pinned snapshots `gpt-4o-2024-11-20` and
`gpt-4o-mini-2024-07-18`; results on other models or dates may drift.

## License

Dual-licensed by directory:

- **Dataset** (`dataset/`, `docs/`): [CC BY 4.0](LICENSE)
- **Code** (`scripts/`): [MIT](LICENSE-CODE)

## Citation

```bibtex
@inproceedings{narula2026escalation,
  author    = {Narula, Bhavya and Mitra, Reshmi},
  title     = {The Escalation Trap: Securing Consumer Voice Agents Against
               Social Engineering},
  year      = {2026},
  note      = {Submitted to IEEE CCNC 2027. Dataset:
               https://github.com/classiccone/voice-agent-dataset}
}
```

See also [CITATION.cff](CITATION.cff) and the full dataset documentation in
[DATASHEET.md](DATASHEET.md).
