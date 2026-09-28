"""SHA-256 helpers backed by Python's standard-library implementation."""

from __future__ import annotations

import hashlib

from utils.helpers import text_to_bytes


def hash_bytes(data: bytes) -> str:
	"""Return the lowercase SHA-256 digest for bytes as hexadecimal text."""
	if not isinstance(data, bytes):
		raise TypeError("data must be bytes")
	return hashlib.sha256(data).hexdigest()


def hash_text(text: str) -> str:
	"""Return the lowercase SHA-256 digest for UTF-8 text."""
	return hash_bytes(text_to_bytes(text))


def sha256(data: str | bytes) -> str:
	"""Hash either UTF-8 text or bytes and return a hexadecimal digest."""
	return hash_text(data) if isinstance(data, str) else hash_bytes(data)
