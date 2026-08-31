# Datasheet: Voice-Agent Social-Engineering Benchmark

Following Gebru et al., *"Datasheets for Datasets"* (CACM 2021). Fields that
the study's source materials do not answer are marked **Not recorded**.

## Motivation

**For what purpose was the dataset created?**
To measure how much protection prompt-layer guardrails give consumer-facing,
LLM-backed voice agents against spoken social-engineering attacks, in the
common "record-in-prompt" architecture where the customer's record is
pre-loaded into the agent's system prompt before identity verification. At the
time of collection there was no public dataset of spoken, single-request
goal-hijacking attacks against customer-service voice agents. The dataset
supports the paper *"The Escalation Trap: Securing Consumer Voice Agents
Against Social Engineering"* (Narula and Mitra, submitted to IEEE CCNC 2027).

**Who created the dataset and on behalf of which entity?**
Bhavya Narula (student researcher) and Dr. Reshmi Mitra (principal
investigator), Department of Computer Science, Southeast Missouri State
University.

**Who funded the creation of the dataset?** Not recorded.

## Composition

**What do the instances represent?**
Single-request spoken phone-call utterances directed at a fictional AI
receptionist ("Maya") for a fictional dental practice. Every utterance targets
exactly one of three commands: C1 read patient notes (information disclosure),
C2 change the contact number (unauthorized account action), or C3 transfer to
the office manager (escalation abuse).

**How many instances are there?**
320 WAV files (16 kHz mono, ~49 minutes total, mean 9.2 s per clip), each with
a cached Whisper transcript and a manifest row.

**What does each instance consist of?**
- `dataset/audio/<id>.wav` — the recording, 16 kHz mono PCM.
- `dataset/transcripts/<id>.json` — the cached Whisper (base) transcript used
  by every evaluation condition.
- A row in `dataset/manifest.csv`: filename, speaker (S1–S8), type
  (LEG/IMP/MAN), subtype (legitimate, direct_claim, or one of eight
  manipulation tactics), command (C1–C3), duration, sample rate, SHA-256.

**Is there a label or target associated with each instance?**
Yes: legitimacy (45 legitimate / 275 adversarial), attack type, tactic
subtype, and target command. Legitimate samples have expected agent response
GRANT; adversarial samples have expected response DENY.

**Category breakdown** (from the manifest): legitimate 45; impersonation
(direct_claim) 66; manipulation 209 — authority_pressure 32, urgency 29,
familiarity_claim 26, escalation_threat 25, prior_verification 25,
confusion_framing 24, emotional_appeal 24, technical_bypass 24.

**Speaker breakdown:** S1 45 (all legitimate), S2 30 (impersonation), S3 30
(manipulation), S4 21 (impersonation), S5 67 (manipulation), S6 66
(manipulation), S7 46 (manipulation), S8 15 (impersonation). All 45 legitimate
samples come from a single speaker (S1); see Limitations.

**Does the dataset contain confidential or personal data?**
No real personal data. All scripts are fictional and reference a fictional
patient record ("Sarah Mitchell"). Speakers are identified only by anonymous
IDs (S1–S8); no key linking identity to recordings is maintained. The raw
audio is a voice recording, so a speaker could in principle be recognized by
someone who knows them; participants consented to public release with this
disclosed.

**Does the dataset rely on external resources?** No; it is self-contained.

## Collection Process

**How was the data collected?**
Adult volunteers read short scripted phone-call lines aloud while being
recorded. Scripts were authored by the research team (a master sample log with
per-sample script text, tactic label, target command, and expected response).
Recording guidance specified a quiet room, a consistent microphone at 6–12
inches, and consistent settings per speaker. Sessions took a few minutes per
speaker.

**Over what timeframe?** May–July 2026 (recording, conversion, and
quality-control artifacts in the source materials are dated in this range).

**Ethical review.**
The Southeast Missouri State University IRB Human Subjects Research
Determination Worksheet was completed by the PI (Dr. Reshmi Mitra, Associate
Professor, Computer Science). As filled, the worksheet records that the
activity is a systematic investigation intended to contribute to generalizable
knowledge (Section I: yes/yes) and that it involves interaction with
individuals and the handling of audio recordings (Section II: yes/yes) — i.e.,
per the worksheet's own decision rule, human subjects research to be submitted
for IRB review. A formal IRB approval or exemption letter is **not among the
source materials; Not recorded**.

**Consent.**
Each speaker signed a consent form stating: participation is voluntary;
participants are 18 or older; they read fictional scripts containing no real
personal information; recordings are labeled only with an anonymous ID and no
identity key is kept; recordings will be combined into a **public research
dataset shared openly** for voice-agent security research; recordings can be
withdrawn any time before public release but not after; and a voice may be
recognizable to people who know the speaker even without a name attached.

**Who was involved in the collection and how were they compensated?**
Volunteer speakers recruited by the research team. Compensation: Not recorded
(the consent form describes participation as voluntary with no direct
benefit).

## Preprocessing / Labeling

**What preprocessing was done?**
- Original recordings were captured per speaker as m4a/AAC (44.1 kHz stereo,
  e.g. phone voice memos) or WAV, then converted and normalized to 16 kHz mono
  WAV and renamed to the release schema.
- Each recording was quality-checked by transcribing it and comparing the
  transcript to the intended script (similarity scoring plus ear-checks);
  takes that failed review were re-recorded, and duplicate-filename collisions
  in the collection sheet were renumbered.
- Transcripts were generated once with local Whisper *base* and cached, so
  every guardrail condition scores the exact same text
  (`dataset/transcripts/`).
- Labels: type/command are encoded in filenames. Thirty S3 manipulation
  samples were collected without a tactic code in the filename; their tactic
  labels were assigned in a reviewed relabeling pass (the labels used for the
  paper's results) and are carried in the manifest. One filename uses the
  legacy code `THR` for escalation_threat.
- The impersonation taxonomy was consolidated to a single pattern
  (direct_claim); a provisional "fabricated prior session" impersonation
  sub-pattern was dropped during label review.

**Was the raw data saved?** The original m4a/WAV takes are retained by the
authors outside this repository. Not distributed.

## Uses

**What tasks can the dataset be used for?**
Benchmarking the resistance of transcript-based (cascaded STT → LLM) voice
agents to spoken social-engineering attacks; measuring guardrail-prompt
effectiveness; studying escalation abuse and security–usability tradeoffs
(verification friction on legitimate callers); speech-security research on
scripted adversarial dialogue.

**Has it been used already?**
Yes — for the accompanying paper's evaluation: five cumulative guardrail
levels (L0–L4), clause-level ablations, a length control, and a minimal
three-rule prompt, scored on two pinned OpenAI snapshots
(`gpt-4o-2024-11-20`, `gpt-4o-mini-2024-07-18`). Per-call results are in
`results/`.

**Limitations — read before using.** In plain language:

- **The content is scripted and synthetic.** Speakers read attack lines
  written by the research team; these are not recordings of real attacks or
  real callers, and delivery may be less varied than genuine adversarial
  speech.
- **Single domain.** Everything targets one fictional dental practice with one
  fictional patient record. Results may not transfer to banking, telecom, or
  other domains.
- **Single turn.** Each sample is one utterance and the evaluation stops at
  the agent's first decision. Multi-turn manipulation, which is where social
  engineering has the most room, is out of scope.
- **Scored against pinned model snapshots.** The released results were
  produced against `gpt-4o-2024-11-20` and `gpt-4o-mini-2024-07-18`. Model
  behavior drifts across snapshots and time, so re-runs on other models or
  dates will not exactly match.
- **Legitimate-caller metrics rest on a single voice.** All 45 legitimate
  samples were recorded by one speaker (S1). Friction metrics computed on the
  legitimate subset (FRR, FVR, LSR) therefore reflect one voice reading
  scripted lines, not a population of real callers.
- **Semantic attacks only.** The pipeline scores the transcript, not the
  waveform. Voice cloning, acoustic spoofing, and prosody-based attacks are
  not represented.

**Uses to avoid.**
Do not use the recordings to build or evaluate speaker-identification systems
aimed at identifying the volunteer speakers, and do not attempt to
re-identify them. The attack scripts are published for defensive research and
reproducibility.

## Distribution

**How is the dataset distributed?**
Publicly, via this GitHub repository:
https://github.com/classiccone/voice-agent-dataset

**License.** Dataset (`dataset/`, `docs/`): CC BY 4.0. Code (`scripts/`): MIT.

**Are there export controls or other restrictions?** None known.

## Maintenance

**Who maintains the dataset?**
The authors (Bhavya Narula and Dr. Reshmi Mitra, Southeast Missouri State
University). Contact: via GitHub issues on this repository.

**Will the dataset be updated?**
Errata (label fixes, documentation corrections) may be published in this
repository; the audio itself is frozen at 320 samples as evaluated in the
paper. Per the consent terms, recordings cannot be withdrawn after public
release, but the maintainers will remove a speaker's recordings from future
versions if a serious concern is raised.

**Version.** v1.0 — the dataset exactly as evaluated in the submitted paper.
