"""Unmodifiable list implementation similar to Collections.unmodifiableList in Java"""

from .unmodifiable import (
    ImmutableList,
    UnsupportedOperationException,
    unmodifiable_list,
)

__all__ = ["ImmutableList", "unmodifiable_list", "UnsupportedOperationException"]

__version__ = "1.0.0"
