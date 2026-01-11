"""
HTTP client for communicating with the text-to-skeleton FastAPI service
"""

import logging
import requests

logger = logging.getLogger(__name__)

FASTAPI_BASE_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 30


class SkeletonServiceError(Exception):
    """Raised when the skeleton service is unavailable or returns an error"""

    pass


def is_service_available():
    """Check if the FastAPI service is running"""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except (requests.exceptions.RequestException, ConnectionError, TimeoutError) as e:
        logger.debug("Service availability check failed: %s", e)
        return False


def get_gloss_sequence(text):
    """Get gloss sequence from /text-to-gloss endpoint"""
    try:
        response = requests.get(
            f"{FASTAPI_BASE_URL}/text-to-gloss",
            params={"text": text},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        glosses = response.json()
        # Extract lemmas from the gloss tuples
        return [gloss[1] for gloss in glosses[0]] if glosses else []
    except requests.exceptions.RequestException as e:
        raise SkeletonServiceError(f"Failed to get gloss sequence: {e}")


def generate_pose(text):
    """Generate pose file via /text-to-pose endpoint"""
    try:
        response = requests.get(
            f"{FASTAPI_BASE_URL}/text-to-pose",
            params={"text": text},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return True  # Pose generated successfully
    except requests.exceptions.RequestException as e:
        raise SkeletonServiceError(f"Failed to generate pose: {e}")
