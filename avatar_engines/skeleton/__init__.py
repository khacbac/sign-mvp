"""
Skeleton Avatar Engine - FastAPI Integration
"""

from .client import (
    is_service_available,
    get_gloss_sequence,
    generate_pose,
    SkeletonServiceError,
)

__all__ = [
    "is_service_available",
    "get_gloss_sequence",
    "generate_pose",
    "SkeletonServiceError",
]
