# Speech-to-Sign Language MVP — Progress Log

This document tracks **what has been completed so far** in the Speech-to-Sign Language MVP project.
It will be **updated incrementally** as new phases are implemented.

---

## 📌 Project Overview

**Goal:**
Build a minimal viable product (MVP) that:

1. Accepts an uploaded audio file
2. Converts speech to text (ASR)
3. Converts text into sign-language-friendly gloss
4. Displays corresponding sign language visuals (videos)

**Current Scope:**

- Sign Language: **American Sign Language (ASL)**
- Sign assets: **Public ASL dictionary videos**
- Focus: correctness, clarity, and explainability (course project)

---

## 🧭 Phase Breakdown

| Phase   | Name                      | Status       |
| ------- | ------------------------- | ------------ |
| Phase 0 | Environment Setup (Conda) | ✅ Completed |
| Phase 1 | Speech-to-Text (ASR)      | ✅ Completed |
| Phase 2 | Text → Gloss              | ⏳ Pending   |
| Phase 3 | Sign Assets (ASL Videos)  | ⏳ Pending   |
| Phase 4 | Sign Rendering            | ⏳ Pending   |
| Phase 5 | Full Integration          | ⏳ Pending   |

---

## 🔹 Phase 0 — Environment Setup (Completed)

### Objective

Create a clean, reproducible Python environment using **Conda**.

### Key Decisions

- Python version pinned to **3.10** for stability
- Conda used for system-level dependencies
- Pip used for ML libraries

### Environment Creation

```bash
conda create -n sign_mvp_clean python=3.10 -y
conda activate sign_mvp_clean
```

### Dependencies Installed

```bash
conda install -c conda-forge ffmpeg opencv -y
pip install "numpy<2.4"
pip install torch torchvision torchaudio
pip install openai-whisper
```

### Environment Export

```bash
conda env export --from-history > environment.yml
```

This ensures:

- Minimal dependency list
- No environment bloat
- Easy reproduction on other machines

---

## 🔹 Phase 1 — Speech-to-Text (ASR) (Completed)

### Objective

Convert an input audio file into plain text using a pretrained model.

### Technology Used

- **OpenAI Whisper (base model)**
- No training or fine-tuning
- Offline inference

### Input / Output

**Input:**

- Audio file (e.g. `input/audio.wav`)

**Output:**

```text
I want to drink water
```

---

### Implementation File

```
asr/transcribe.py
```

### Key Implementation Notes

- Whisper model is loaded once per execution
- Audio path is passed via command-line argument
- Output text is printed to terminal

### macOS Compatibility Fix

To avoid OpenMP runtime conflicts:

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
```

This line must appear **before importing Whisper**.

---

### How to Run

```bash
conda activate sign_mvp_clean
python asr/transcribe.py input/audio.wav
```

### Example Output

```text
[INFO] Loading Whisper model...
[INFO] Transcribing audio: input/audio.wav

=== TRANSCRIPTION RESULT ===
I want to drink water
```

---

### Conceptual Flow (Phase 1)

```
Audio File
   ↓
Feature Extraction (Mel Spectrogram)
   ↓
Whisper Transformer Model
   ↓
Plain Text Output
```

---

### Report-Ready Description

> Speech recognition is implemented using OpenAI’s Whisper pretrained model. Given an uploaded audio file, the system performs offline inference to convert spoken language into text. The transcription output is returned as plain text and serves as input for subsequent text processing and sign language translation stages.

---

## 📁 Current Project Structure

```
sign_mvp/
│
├── asr/
│   └── transcribe.py
├── input/
│   └── audio.wav
├── environment.yml
└── README.md  (this file)
```

---

## 🔜 Next Planned Phase

### Phase 2 — Text → Gloss (Rule-Based NLP)

**Goal:**

- Convert spoken-language text into sign-language-friendly gloss tokens

**Why Rule-Based?**

- No training required
- Fully explainable
- Ideal for MVP and academic evaluation

This document will be **updated after Phase 2 is completed**.

---

_Last updated: Phase 1 completed (ASR working)_
