#!/usr/bin/env python3
"""
Script to generate ASE sign language pose files and update the lexicon CSV.

Usage:
    python generate_poses.py word1 word2 "multi word phrase"
    python generate_poses.py --split "sentence to split into words"
"""

import os
import sys
import csv
import re
from pathlib import Path
from urllib.parse import quote
import requests
from typing import List, Tuple


def generate_filename(text: str) -> str:
    """
    Convert text to a safe filename.

    Args:
        text: The input text (e.g., "how are you")

    Returns:
        Filename without extension (e.g., "how-are-you")
    """
    # Convert to lowercase and replace spaces with hyphens
    filename = text.strip().lower()
    filename = re.sub(r'\s+', '-', filename)
    # Remove any characters that aren't alphanumeric, hyphens, or underscores
    filename = re.sub(r'[^a-z0-9\-_]', '', filename)
    return filename


def download_pose(word: str, output_path: Path) -> bool:
    """
    Download pose file from the API.

    Args:
        word: The word or phrase to download
        output_path: Where to save the pose file

    Returns:
        True if successful, False otherwise
    """
    url = f"https://us-central1-sign-mt.cloudfunctions.net/spoken_text_to_signed_pose?text={quote(word)}&spoken=en&signed=ase"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Validate that we got actual content
        if len(response.content) == 0:
            print(f"  ✗ Error: API returned empty file")
            return False

        # Save the file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True

    except requests.exceptions.Timeout:
        print(f"  ✗ Error: Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def read_csv(csv_path: Path) -> List[List[str]]:
    """Read the CSV file and return rows."""
    if not csv_path.exists():
        # Return header only if file doesn't exist
        return [["path", "spoken_language", "signed_language", "start", "end", "words", "glosses", "priority"]]

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)


def entry_exists(rows: List[List[str]], path: str) -> bool:
    """Check if an entry with the given path already exists in CSV."""
    for row in rows[1:]:  # Skip header
        if row and row[0] == path:
            return True
    return False


def add_csv_entry(csv_path: Path, filename: str, word: str, gloss: str) -> bool:
    """
    Add a new entry to the CSV file.

    Args:
        csv_path: Path to the CSV file
        filename: The pose filename (e.g., "hello.pose")
        word: The original word/phrase (e.g., "hello" or "how are you")
        gloss: The gloss representation (e.g., "hello" or "how-are-you")

    Returns:
        True if successful, False otherwise
    """
    try:
        rows = read_csv(csv_path)

        # Check if entry already exists
        relative_path = f"ase/{filename}"
        if entry_exists(rows, relative_path):
            return True

        # Add new entry
        new_row = [relative_path, "en", "ase", "0", "0", word, gloss, "0"]
        rows.append(new_row)

        # Write back to CSV
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return True

    except Exception as e:
        print(f"  ✗ Error updating CSV: {str(e)}")
        return False


def process_words(words: List[str]) -> Tuple[int, int, int]:
    """
    Process a list of words.

    Args:
        words: List of words/phrases to process

    Returns:
        Tuple of (generated_count, skipped_count, failed_count)
    """
    # Get paths
    script_dir = Path(__file__).parent
    ase_dir = script_dir / "assets" / "lexicon" / "ase"
    csv_path = script_dir / "assets" / "lexicon" / "index.csv"

    generated = 0
    skipped = 0
    failed = 0

    print(f"Processing {len(words)} word(s)...\n")

    for i, word in enumerate(words, 1):
        print(f"[{i}/{len(words)}] {word}")

        # Generate filename
        filename_base = generate_filename(word)
        filename = f"{filename_base}.pose"
        pose_path = ase_dir / filename

        # Check if file already exists
        if pose_path.exists():
            print(f"  ⊘ Skipped (already exists: ase/{filename})")
            skipped += 1
            continue

        # Download the pose file
        print(f"  → Downloading pose for \"{word}\"...")
        if download_pose(word, pose_path):
            print(f"  ✓ Saved to ase/{filename}")

            # Update CSV
            if add_csv_entry(csv_path, filename, word, filename_base):
                print(f"  ✓ Added to index.csv")
                generated += 1
            else:
                failed += 1
        else:
            failed += 1

        print()  # Empty line for readability

    return generated, skipped, failed


def split_into_words(text: str) -> List[str]:
    """
    Split text into individual words, removing punctuation.

    Args:
        text: Input text to split

    Returns:
        List of individual words (lowercase, no punctuation)
    """
    # Remove punctuation and split by whitespace
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python generate_poses.py [OPTIONS] word1 word2 ...")
        print("\nOptions:")
        print("  --split    Split sentences into individual words")
        print("\nExamples:")
        print("  # Generate poses for individual words:")
        print("  python generate_poses.py hello world goodbye")
        print("")
        print("  # Generate pose for a phrase:")
        print("  python generate_poses.py \"how are you\"")
        print("")
        print("  # Split sentence into individual words:")
        print("  python generate_poses.py --split \"how are you\"")
        print("  # This will generate: how.pose, are.pose, you.pose")
        sys.exit(1)

    # Check for --split flag
    split_mode = False
    args = sys.argv[1:]

    if args[0] == '--split':
        split_mode = True
        args = args[1:]

    if not args:
        print("Error: No words provided")
        sys.exit(1)

    # Process words based on mode
    if split_mode:
        # Split all arguments into individual words
        all_words = []
        for arg in args:
            all_words.extend(split_into_words(arg))
        # Remove duplicates while preserving order
        words = list(dict.fromkeys(all_words))
        print(f"Split mode: Processing {len(words)} unique word(s) from input\n")
    else:
        words = args

    generated, skipped, failed = process_words(words)

    # Print summary
    print("Summary:")
    print(f"  ✓ {generated} generated")
    print(f"  ⊘ {skipped} skipped")
    print(f"  ✗ {failed} failed")

    # Exit with error code if any failed
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
