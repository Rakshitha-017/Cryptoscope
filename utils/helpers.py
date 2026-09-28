"""Input, conversion, and display helpers shared by the algorithm pages."""

from __future__ import annotations


def text_to_bytes(text: str) -> bytes:
	"""Encode text as UTF-8 bytes."""
	if not isinstance(text, str):
		raise TypeError("text must be a string")
	return text.encode("utf-8")


def bytes_to_int(data: bytes) -> int:
	"""Convert bytes to a non-negative big-endian integer."""
	if not isinstance(data, bytes):
		raise TypeError("data must be bytes")
	return int.from_bytes(data, "big")


def int_to_bytes(value: int, length: int | None = None) -> bytes:
	"""Convert a non-negative integer to big-endian bytes."""
	if value < 0:
		raise ValueError("value must be non-negative")
	minimum_length = max(1, (value.bit_length() + 7) // 8)
	output_length = minimum_length if length is None else length
	if output_length < minimum_length:
		raise ValueError("length is too small for value")
	return value.to_bytes(output_length, "big")


def validate_positive_integer(value: int, name: str = "value") -> None:
	"""Raise ``ValueError`` unless ``value`` is a positive integer."""
	if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
		raise ValueError(f"{name} must be a positive integer")


def format_hex(value: int | bytes) -> str:
	"""Format an integer or bytes value as a lowercase hexadecimal string."""
	if isinstance(value, int):
		if value < 0:
			raise ValueError("value must be non-negative")
		return f"{value:x}"
	if isinstance(value, bytes):
		return value.hex()
	raise TypeError("value must be an integer or bytes")
