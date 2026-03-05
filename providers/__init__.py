"""
Provider for Speech-to-Text via Ancroo Backend.

Ancroo Voice connects exclusively to the Ancroo Backend. Model and STT server
selection is handled entirely server-side — clients only send audio and language.
"""

from .ancroo_backend import AncrooBackendProvider

__all__ = [
    'AncrooBackendProvider',
]
