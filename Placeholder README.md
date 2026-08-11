# 🎙️ Escalation Trap: Measuring Prompt Guardrail for Securing Voice Agents

**Bhavya Narula, Reshmi Mitra, Roy David Kakwenga, Debayan Dutta**  
Southeast Missouri State University, Cape Girardeau, USA

> A research testbed and voice dataset for evaluating prompt-layer guardrails against spoken social-engineering attacks on AI voice agents.

---

## 🔍 Overview

**Escalation Trap** studies the security of LLM-backed customer-service voice agents in a controlled setting. The project focuses on how spoken social-engineering attempts interact with prompt-level identity-verification and access-control rules.

The repository is intended to support reproducible research on:

- Voice-agent security
- Prompt-layer guardrails
- Social-engineering resistance
- Identity-verification behavior
- Security/usability tradeoffs

The accompanying paper contains the full methodology, experimental design, analysis, and results.

---

## 📦 Dataset

The **Voice-Agent Dataset for Prompt-Layer Guardrails** contains:

- **320** audio recordings
- **8** speakers
- **16 kHz mono WAV** audio
- Legitimate and adversarial customer-service requests
- A fictional dental-practice scenario
- Synthetic customer information only

The recordings were created specifically for this research project and were not collected from a public dataset.

### File naming

Audio files use structured filenames that identify the speaker, request type, target category, and recording number.

Examples:

```text
S4_IMP_C2_01.wav
S7_MAN_C3_FAM_05.wav
```

See the dataset documentation for the complete naming convention and category definitions.

---

## 📁 Repository Structure

```text
Escalation-Trap/
├── datasets/
├── scripts/
├── docs/
├── README.md
├── LICENSE
```

### `datasets/`
Contains the released voice-agent dataset and related dataset files.

### `scripts/`
Contains the scripts used to prepare, process, transcribe, evaluate, and analyze the dataset.

### `docs/`
Contains supporting documentation for the dataset and research project.

The public repository is intentionally kept compact so that the main research materials are easy to locate without exposing private development files or participant-identifying information.

---

## 🧪 Research Testbed

At a high level, the testbed follows this workflow:

```text
Voice sample
    ↓
Speech transcription
    ↓
Voice-agent decision model
    ↓
Prompt guardrail policy
    ↓
Structured security evaluation
```

The repository includes scripts for preparing the dataset, validating audio files, transcribing samples, running evaluations, and aggregating results.

For complete experimental settings and benchmark results, please refer to the accompanying paper.

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone <YOUR-REPOSITORY-URL>
cd Escalation-Trap
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Additional usage instructions for individual scripts can be documented inside the `scripts/` folder.

---

## 🔐 Privacy and Ethics

All customer information used in the benchmark is fictional.

Recording participants provided consent for their audio to be used for research and public dataset release. Participants are identified only by speaker number in the released materials.

Because voices may be recognizable to people familiar with a participant, complete anonymity cannot be guaranteed.

---

## 📜 License

The **Voice-Agent Dataset for Prompt-Layer Guardrails** is released under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

Users may share and adapt the dataset for research, educational, and commercial purposes with appropriate attribution.

See `LICENSE` for details.

---

## 📄 Paper

This repository accompanies:

**Escalation Trap: Measuring Prompt Guardrail for Securing Voice Agents**

Bhavya Narula, Reshmi Mitra, Roy David Kakwenga, and Debayan Dutta  
Southeast Missouri State University

The full paper contains the methodology, evaluation metrics, experimental results, discussion, and limitations.

**Paper link:** `to add put final paper url here `

---

## 📌 Citation

If you use the dataset, code, or benchmark in your research, please cite the dataset and accompanying paper.

To add put citation later 
---

## 📬 Contact

For questions about the dataset or research project:

- **Bhavya Narula** — `bnarula1s@semo.edu`
- **Reshmi Mitra** — `rmitra@semo.edu`
- **Roy David Kakwenga** — `rkakwenga1s@semo.edu`
- **Debayan Dutta** — `ddutta1s@semo.edu`

---

## ⚠️ Responsible Use

This repository is intended for defensive security research, reproducibility, and the study of trustworthy AI voice-agent systems.

Users are responsible for ensuring that their use of the dataset and code complies with applicable laws, institutional policies, ethical requirements, and research regulations.
