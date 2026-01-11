# Text-to-Skeleton

A Python module that converts spoken language text into American Sign Language (ASE) pose data and video representations.

## Overview

This module provides a pipeline for converting text to sign language:
1. **Text → Gloss**: Converts spoken language text to glosses using spaCy lemmatization
2. **Gloss → Pose**: Looks up pose data from a lexicon for each gloss
3. **Pose → Video**: Generates video output from pose sequences

## Features

- FastAPI server with REST endpoints for text-to-gloss, text-to-pose, and text-to-video conversion
- Lexicon-based pose lookup with fingerspelling fallback
- Command-line tool for generating and managing pose files
- Support for English to ASE (American Sign Language) conversion

## API Endpoints

The FastAPI server exposes the following endpoints:

### `GET /text-to-gloss`
Converts text to glosses using spaCy lemmatization.

**Parameters:**
- `text` (string): Input text to convert

**Returns:** List of glosses

### `GET /text-to-pose`
Converts text to pose data and saves as a `.pose` file.

**Parameters:**
- `text` (string): Input text to convert

**Returns:** HTTP Response (pose file saved to `output/poses/`)

### `GET /text-to-video`
Converts text to video representation.

**Parameters:**
- `text` (string): Input text to convert

**Returns:** Video file path (saved to `output/videos/sample.mp4`)

## Directory Structure

```
text-to-skeleton/
├── assets/
│   └── lexicon/        # Pose lexicon files
│       ├── ase/        # ASE pose files (.pose)
│       └── index.csv   # Lexicon index
├── output/
│   ├── poses/          # Generated pose files
│   └── videos/         # Generated video files
├── main.py             # FastAPI server
├── generate_poses.py   # CLI tool for managing poses
└── utils.py            # Text-to-gloss utilities
```

## Usage

### Starting the Server

```bash
uvicorn main:app --reload
```

The server will start with CORS enabled for all origins.

### Generating Pose Files

Use the `generate_poses.py` script to download pose files and add them to the lexicon:

```bash
# Generate poses for individual words
python generate_poses.py hello world goodbye

# Generate pose for a phrase
python generate_poses.py "how are you"

# Split sentence into individual words
python generate_poses.py --split "how are you"
```

The script will:
- Download pose files from the Sign MT API
- Save them to `assets/lexicon/ase/`
- Update `assets/lexicon/index.csv` with the new entries
- Skip existing poses automatically

## Dependencies

- FastAPI
- spoken-to-signed library
- spaCy with language models (en_core_web_lg)
- requests (for pose generation)

## How It Works

1. **Text Processing**: Input text is processed using spaCy to extract lemmas (base forms of words)
2. **Gloss Lookup**: Each lemma is looked up in the CSV-based lexicon
3. **Fingerspelling Fallback**: If a word is not found in the lexicon, fingerspelling is used as a backup
4. **Pose Assembly**: Individual poses are assembled into a sequence
5. **Video Generation**: The pose sequence is rendered to video (optional)

## Configuration

- **Spoken Language**: English (en)
- **Signed Language**: American Sign Language (ase)
- **API Endpoint**: `https://us-central1-sign-mt.cloudfunctions.net/spoken_text_to_signed_pose`

## Notes

- Pose files are stored in the `.pose` format
- The lexicon CSV contains metadata: path, languages, timing, words, glosses, and priority
- Static files in `output/` directory are served via FastAPI
