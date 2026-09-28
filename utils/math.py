"""Small integer-math helpers used by the educational crypto modules."""

from __future__ import annotations

import random


def modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
	"""Return ``base ** exponent % modulus`` using square-and-multiply."""
	if modulus <= 0:
		raise ValueError("modulus must be positive")
	if exponent < 0:
		raise ValueError("exponent must be non-negative")
	return pow(base, exponent, modulus)


mod_exp = modular_exponentiation


def gcd(first: int, second: int) -> int:
	"""Return the greatest common divisor of two integers."""
	while second:
		first, second = second, first % second
	return abs(first)


def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
	"""Return ``(gcd, coefficient_for_first, coefficient_for_second)``."""
	old_r, remainder = first, second
	old_s, coefficient_s = 1, 0
	old_t, coefficient_t = 0, 1
	while remainder:
		quotient = old_r // remainder
		old_r, remainder = remainder, old_r - quotient * remainder
		old_s, coefficient_s = coefficient_s, old_s - quotient * coefficient_s
		old_t, coefficient_t = coefficient_t, old_t - quotient * coefficient_t
	if old_r < 0:
		return -old_r, -old_s, -old_t
	return old_r, old_s, old_t


def modular_inverse(value: int, modulus: int) -> int:
	"""Return the inverse of ``value`` modulo ``modulus``."""
	if modulus <= 1:
		raise ValueError("modulus must be greater than one")
	common, coefficient, _ = extended_gcd(value, modulus)
	if common != 1:
		raise ValueError("value has no modular inverse")
	return coefficient % modulus


mod_inverse = modular_inverse


def is_prime(candidate: int) -> bool:
	"""Return whether ``candidate`` is prime using deterministic trial division."""
	if candidate < 2:
		return False
	if candidate in (2, 3):
		return True
	if candidate % 2 == 0:
		return False
	divisor = 3
	while divisor * divisor <= candidate:
		if candidate % divisor == 0:
			return False
		divisor += 2
	return True


def generate_prime(bits: int = 16, rng: random.Random | None = None) -> int:
	"""Generate a small probable prime for demonstrations and tests."""
	if bits < 2:
		raise ValueError("bits must be at least two")
	source = rng or random.SystemRandom()
	while True:
		candidate = source.getrandbits(bits) | (1 << (bits - 1)) | 1
		if is_prime(candidate):
			return candidate

