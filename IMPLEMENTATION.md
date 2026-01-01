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

## 🔹 Phase 2 — Text → Gloss (Rule-Based NLP) (Completed)

### Objective

Convert natural language text into **sign-language-friendly gloss tokens**.

This phase bridges **speech recognition (Phase 1)** and **sign rendering (later phases)**.

---

## 🧠 Design Rationale

Sign languages do not follow spoken-language grammar. Instead of translating word-for-word, we convert text into **gloss**:

- Uppercase keywords
- Simplified structure
- Removal of unnecessary function words

This MVP uses a **rule-based approach**:

- No machine learning
- Fully explainable
- Deterministic output

---

## 🔤 Input / Output

**Input (from Phase 1):**

```text
I want to drink water
```

**Output (Gloss Tokens):**

```text
[I, WANT, WATER]
```

---

## 🪜 Processing Steps

1. Convert text to lowercase
2. Remove punctuation
3. Tokenize text into words
4. Remove stopwords (e.g., "to", "the", "is", "drink")
5. Convert remaining words to uppercase

---

## 📁 Implementation File

```
nlp/text_to_gloss.py
```

---

## 🧩 Stopword Strategy

Stopwords are words that:

- Do not contribute to sign meaning
- Are often omitted in sign language

### Example Stopwords

```
{"to", "the", "a", "an", "is", "are", "am", "drink", "do"}
```

This list is **manually defined** and can be easily extended.

---

## 🧪 Testing Examples

| Input Sentence        | Gloss Output           |
| --------------------- | ---------------------- |
| I want water          | [I, WANT, WATER]       |
| Hello I want food     | [HELLO, I, WANT, FOOD] |
| I want to drink water | [I, WANT, WATER]       |

---

## 🧠 Conceptual Flow (Phase 2)

```
Text Output (ASR)
   ↓
Rule-Based Filtering
   ↓
Gloss Tokens
```

---

## 📝 Report-Ready Description

> The text-to-gloss module converts transcribed speech into a simplified gloss representation suitable for sign language rendering. A rule-based approach is adopted to remove non-essential function words and normalize remaining keywords into uppercase gloss tokens. This design ensures full transparency and ease of explanation for an MVP system.

---

## 🔹 Phase 3 — Sign Assets (ASL Video Collection & Mapping) (Completed)

### Objective

Prepare **visual sign language assets** and map gloss tokens to corresponding ASL videos.

This phase enables the system to convert abstract gloss tokens into **concrete visual representations**.

---

## 🧠 Design Rationale

Instead of generating sign videos (which is complex and data-intensive), this MVP:

- Uses **pre-recorded ASL videos** from public educational dictionaries
- Maps each gloss token to a short video clip
- Plays videos sequentially in later phases

This approach:

- Avoids video synthesis
- Requires no model training
- Is reliable and easy to demonstrate

---

## 📦 Sign Vocabulary (MVP)

For the MVP, a small but expressive vocabulary is sufficient.

### Selected Gloss Tokens

```
I
YOU
WANT
NEED
WATER
FOOD
HELLO
THANK
YES
NO
```

These words allow multiple meaningful demo sentences.

---

## 📁 Asset Directory Structure

```
sign_mvp/
│
├── signs/
│   └── videos/
│       ├── I.mp4
│       ├── WANT.mp4
│       ├── WATER.mp4
│       ├── HELLO.mp4
│       └── ...
```

---

## 🎥 Video Collection Guidelines

- Source: public ASL educational dictionaries (e.g. Lifeprint)
- Format: `.mp4`
- Duration: 1–3 seconds per sign
- Resolution: any (OpenCV will handle scaling)
- Naming: **UPPERCASE**, matches gloss exactly

---

## 🗂 Gloss-to-Video Mapping

### Mapping File

```
mapping/gloss_to_video.json
```

### Example Content

```json
{
  "I": "I.mp4",
  "YOU": "YOU.mp4",
  "WANT": "WANT.mp4",
  "WATER": "WATER.mp4",
  "FOOD": "FOOD.mp4",
  "HELLO": "HELLO.mp4",
  "THANK": "THANK.mp4"
}
```

This file decouples **language processing** from **visual rendering**.

---

## 🧪 Verification Steps

1. Open each video manually to ensure it plays correctly
2. Confirm filenames exactly match gloss tokens
3. Validate JSON format (no trailing commas)

---

## 🧠 Conceptual Flow (Phase 3)

```
Gloss Tokens
   ↓
Gloss-to-Video Mapping
   ↓
ASL Video Assets
```

---

## 📝 Report-Ready Description

> To visualize sign language output, the system uses pre-recorded ASL sign videos sourced from public educational dictionaries. Each gloss token is mapped to a corresponding video file using a simple lookup table. This design avoids the complexity of video generation while enabling a clear and effective demonstration of speech-to-sign translation.

---

## 🔹 Phase 4 — Sign Rendering (Video Playback) (Completed)

### Objective

Render sign language output by **playing ASL videos sequentially** according to the gloss order.

This phase converts symbolic gloss tokens into **visible sign language output**.

---

## 🧠 Design Rationale

Rather than synthesizing animations or avatars, the MVP:

- Uses OpenCV to play pre-recorded ASL videos
- Displays videos one after another in gloss order
- Keeps rendering logic simple and reliable

This approach is:

- Lightweight
- Cross-platform
- Easy to debug and explain

---

## 📁 Implementation File

```
renderer/play_sign_sequence.py
```

---

## 🔄 Rendering Logic

1. Load gloss-to-video mapping (`gloss_to_video.json`)
2. For each gloss token:

   - Find corresponding video file
   - Load video with OpenCV
   - Display frames sequentially

3. Close video window after playback

---

## 🧩 Key Functions

- `play_video(video_path)` — plays a single ASL video
- `play_gloss_sequence(gloss_list)` — plays a list of videos in order

---

## ⚠️ Missing Gloss Handling

If a gloss token does not exist in the mapping:

- The system prints a warning
- Rendering continues with remaining glosses

This ensures robustness during demos.

---

## 🧠 Conceptual Flow (Phase 4)

```
Gloss Tokens
   ↓
Video Lookup
   ↓
OpenCV Playback
```

---

## 🧪 Example Execution

Input Gloss:

```text
[I, WANT, WATER]
```

Visual Output:

```
I.mp4 → WANT.mp4 → WATER.mp4
```

---

## 📝 Report-Ready Description

> The sign rendering module visualizes sign language output by sequentially playing pre-recorded ASL sign videos using OpenCV. Each gloss token is mapped to a corresponding video file, and videos are displayed in order to simulate continuous sign language communication.

---

## 🔜 Next Planned Phase

### Phase 5 — Full System Integration

**Goal:**

- Connect ASR, gloss conversion, and sign rendering into a single pipeline
- Enable one-command end-to-end execution

This document will be updated after Phase 5 is completed.
