"""
Gloss Mapper for WLASL Dataset

Maps gloss strings to video IDs based on WLASL metadata.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from .config import WLASL_METADATA_PATH, PREFERRED_SOURCES

logger = logging.getLogger(__name__)


class GlossMapper:
    """Maps gloss strings to video IDs using WLASL metadata"""

    def __init__(self, metadata_path: Optional[Path] = None):
        """
        Initialize gloss mapper with WLASL metadata.

        Args:
            metadata_path: Path to WLASL_v0.3.json file
        """
        self.metadata_path = metadata_path or WLASL_METADATA_PATH
        self._gloss_to_videos: Dict[str, List[Dict[str, Any]]] = {}
        self._gloss_vocabulary: Set[str] = set()
        self._load_metadata()

    def _load_metadata(self):
        """Load WLASL metadata from JSON file"""
        try:
            if not self.metadata_path.exists():
                raise FileNotFoundError(f"WLASL metadata not found at {self.metadata_path}")

            logger.info(f"Loading WLASL metadata from {self.metadata_path}")

            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Build gloss to video IDs mapping
            for entry in data:
                gloss = entry['gloss'].upper()  # Convert to uppercase for case-insensitive matching
                videos = entry['instances']

                self._gloss_to_videos[gloss] = videos
                self._gloss_vocabulary.add(gloss)

            logger.info(f"Loaded {len(self._gloss_vocabulary)} glosses with {sum(len(v) for v in self._gloss_to_videos.values())} total videos")

        except Exception as e:
            logger.error(f"Failed to load WLASL metadata: {e}")
            raise

    def get_gloss_vocabulary(self) -> Set[str]:
        """Get set of all available glosses"""
        return self._gloss_vocabulary.copy()

    def gloss_exists(self, gloss: str) -> bool:
        """Check if a gloss exists in the dataset"""
        return gloss.upper() in self._gloss_vocabulary

    def get_video_ids(self, gloss: str) -> List[str]:
        """
        Get all video IDs for a given gloss.

        Args:
            gloss: The sign language gloss (case-insensitive)

        Returns:
            List of video IDs
        """
        gloss_upper = gloss.upper()
        if gloss_upper not in self._gloss_to_videos:
            logger.warning(f"Gloss '{gloss}' not found in WLASL dataset")
            return []

        videos = self._gloss_to_videos[gloss_upper]
        return [video['video_id'] for video in videos]

    def get_video_metadata(self, gloss: str) -> List[Dict[str, Any]]:
        """
        Get all video metadata for a given gloss.

        Args:
            gloss: The sign language gloss (case-insensitive)

        Returns:
            List of video metadata dictionaries
        """
        gloss_upper = gloss.upper()
        return self._gloss_to_videos.get(gloss_upper, [])

    def get_best_video(self, gloss: str) -> Optional[Dict[str, Any]]:
        """
        Get the best video for a given gloss based on preferred sources.

        Args:
            gloss: The sign language gloss (case-insensitive)

        Returns:
            Best video metadata dictionary or None if not found
        """
        videos = self.get_video_metadata(gloss)
        if not videos:
            return None

        # Sort by preferred source order
        for source in PREFERRED_SOURCES:
            for video in videos:
                if video.get('source') == source:
                    return video

        # If no preferred source found, return first video
        return videos[0]

    def get_best_videos_with_alternatives(self, gloss: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Get the best video for a gloss with alternative options for fallback.

        Args:
            gloss: The sign language gloss (case-insensitive)
            max_results: Maximum number of video alternatives to return

        Returns:
            List of video metadata dictionaries sorted by preference
        """
        videos = self.get_video_metadata(gloss)
        if not videos:
            return []

        # Sort videos by source preference
        scored_videos = []
        for video in videos:
            source = video.get('source', '')
            try:
                # Lower score is better (higher in preference list)
                score = PREFERRED_SOURCES.index(source)
            except ValueError:
                # Source not in preferred list, assign low priority
                score = len(PREFERRED_SOURCES) + 1
            scored_videos.append((score, video))

        # Sort by score (preference) and return top results
        scored_videos.sort(key=lambda x: x[0])
        return [video for _, video in scored_videos[:max_results]]

    def get_video_count(self, gloss: str) -> int:
        """
        Get the number of videos available for a gloss.

        Args:
            gloss: The sign language gloss

        Returns:
            Number of videos
        """
        return len(self.get_video_ids(gloss))

    def find_similar_glosses(self, gloss: str, max_results: int = 5) -> List[str]:
        """
        Find glosses similar to the given gloss (for fuzzy matching).

        Args:
            gloss: The gloss to find matches for
            max_results: Maximum number of results to return

        Returns:
            List of similar glosses
        """
        gloss_upper = gloss.upper()
        similar = []

        # Exact match
        if gloss_upper in self._gloss_vocabulary:
            similar.append(gloss_upper)

        # Substring match
        for vocab_gloss in self._gloss_vocabulary:
            if gloss_upper in vocab_gloss or vocab_gloss in gloss_upper:
                if vocab_gloss not in similar:
                    similar.append(vocab_gloss)

        return similar[:max_results]

    def get_all_glosses(self) -> List[str]:
        """Get sorted list of all glosses"""
        return sorted(self._gloss_vocabulary)


# Global mapper instance
_mapper = None


def get_gloss_mapper() -> GlossMapper:
    """Get singleton instance of GlossMapper"""
    global _mapper
    if _mapper is None:
        _mapper = GlossMapper()
    return _mapper


def get_video_ids(gloss: str) -> List[str]:
    """Convenience function to get video IDs for a gloss"""
    return get_gloss_mapper().get_video_ids(gloss)


def get_best_video(gloss: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get best video for a gloss"""
    return get_gloss_mapper().get_best_video(gloss)


def get_best_videos_with_alternatives(gloss: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Convenience function to get best video with alternatives for a gloss"""
    return get_gloss_mapper().get_best_videos_with_alternatives(gloss, max_results)


def gloss_exists(gloss: str) -> bool:
    """Convenience function to check if gloss exists"""
    return get_gloss_mapper().gloss_exists(gloss)


__all__ = [
    "GlossMapper",
    "get_gloss_mapper",
    "get_video_ids",
    "get_best_video",
    "get_best_videos_with_alternatives",
    "gloss_exists",
]
