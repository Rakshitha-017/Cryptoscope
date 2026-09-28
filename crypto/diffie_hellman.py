"""Diffie-Hellman key exchange primitives for educational demonstrations."""

from __future__ import annotations

import secrets
from dataclasses import dataclass

from utils.math import is_prime, modular_exponentiation


@dataclass(frozen=True)
class DHParameters:
	prime: int
	generator: int

	def validate(self) -> None:
		if not is_prime(self.prime):
			raise ValueError("prime must be prime")
		if not 1 < self.generator < self.prime:
			raise ValueError("generator must be between one and prime")


def validate_parameters(prime: int, generator: int) -> None:
	DHParameters(prime, generator).validate()


def generate_private_key(prime: int) -> int:
	"""Generate a private exponent in the valid range for ``prime``."""
	if not is_prime(prime) or prime <= 3:
		raise ValueError("prime must be a prime greater than three")
	return secrets.randbelow(prime - 2) + 2


def calculate_public_key(private_key: int, generator: int, prime: int) -> int:
	"""Calculate ``generator ** private_key mod prime``."""
	validate_parameters(prime, generator)
	if not 1 < private_key < prime - 1:
		raise ValueError("private key must be between one and prime minus one")
	return modular_exponentiation(generator, private_key, prime)


def calculate_shared_secret(private_key: int, other_public_key: int, prime: int) -> int:
	"""Calculate the shared secret from a private key and peer public key."""
	if not is_prime(prime):
		raise ValueError("prime must be prime")
	if not 1 < private_key < prime - 1:
		raise ValueError("private key must be between one and prime minus one")
	if not 1 < other_public_key < prime:
		raise ValueError("public key must be between one and prime")
	return modular_exponentiation(other_public_key, private_key, prime)


def exchange_values(
	private_key: int, other_private_key: int, parameters: DHParameters
) -> dict[str, int]:
	"""Return public keys and shared secrets for lab visualization."""
	parameters.validate()
	public_key = calculate_public_key(private_key, parameters.generator, parameters.prime)
	other_public_key = calculate_public_key(
		other_private_key, parameters.generator, parameters.prime
	)
	shared_secret = calculate_shared_secret(private_key, other_public_key, parameters.prime)
	other_shared_secret = calculate_shared_secret(
		other_private_key, public_key, parameters.prime
	)
	return {
		"public_key": public_key,
		"other_public_key": other_public_key,
		"shared_secret": shared_secret,
		"other_shared_secret": other_shared_secret,
	}
