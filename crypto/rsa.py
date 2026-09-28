"""Educational RSA primitives using deliberately small demonstration keys."""

from __future__ import annotations

from dataclasses import dataclass
import random

from utils.math import gcd, generate_prime, modular_exponentiation, modular_inverse


@dataclass(frozen=True)
class RSAPublicKey:
	exponent: int
	modulus: int


@dataclass(frozen=True)
class RSAPrivateKey:
	exponent: int
	modulus: int


@dataclass(frozen=True)
class RSAKeyPair:
	public: RSAPublicKey
	private: RSAPrivateKey
	p: int
	q: int


def _validate_key(key: RSAPublicKey | RSAPrivateKey) -> None:
	if key.exponent <= 0 or key.modulus <= 1:
		raise ValueError("RSA key values must be positive")


def generate_keypair(
	p: int | None = None,
	q: int | None = None,
	e: int = 65537,
	bits: int = 16,
	rng: random.Random | None = None,
) -> RSAKeyPair:
	"""Generate an RSA key pair; small explicit primes are useful in the lab."""
	source = rng or random.SystemRandom()
	first_prime = p if p is not None else generate_prime(bits, source)
	second_prime = q if q is not None else generate_prime(bits, source)
	if first_prime == second_prime:
		raise ValueError("p and q must be distinct")
	from utils.math import is_prime

	if not is_prime(first_prime) or not is_prime(second_prime):
		raise ValueError("p and q must both be prime")
	if e <= 1:
		raise ValueError("public exponent must be greater than one")
	modulus = first_prime * second_prime
	totient = (first_prime - 1) * (second_prime - 1)
	if gcd(e, totient) != 1:
		raise ValueError("public exponent must be coprime to the totient")
	private_exponent = modular_inverse(e, totient)
	return RSAKeyPair(
		public=RSAPublicKey(e, modulus),
		private=RSAPrivateKey(private_exponent, modulus),
		p=first_prime,
		q=second_prime,
	)


generate_keys = generate_keypair


def encrypt(message: int, key: RSAPublicKey) -> int:
	"""Encrypt an integer message smaller than the public modulus."""
	_validate_key(key)
	if not isinstance(message, int) or message < 0 or message >= key.modulus:
		raise ValueError("message must be an integer in the RSA modulus range")
	return modular_exponentiation(message, key.exponent, key.modulus)


def decrypt(ciphertext: int, key: RSAPrivateKey) -> int:
	"""Decrypt an integer ciphertext in the private key's modulus range."""
	_validate_key(key)
	if not isinstance(ciphertext, int) or ciphertext < 0 or ciphertext >= key.modulus:
		raise ValueError("ciphertext must be an integer in the RSA modulus range")
	return modular_exponentiation(ciphertext, key.exponent, key.modulus)


def sign(message: int, key: RSAPrivateKey) -> int:
	"""Create a toy RSA signature for an integer message representative."""
	return decrypt(message, key)


def verify(message: int, signature: int, key: RSAPublicKey) -> bool:
	"""Verify a toy RSA signature for an integer message representative."""
	try:
		return encrypt(signature, key) == message
	except ValueError:
		return False


def intermediate_values(key_pair: RSAKeyPair) -> dict[str, int]:
	"""Return RSA values useful for educational visualization."""
	return {
		"p": key_pair.p,
		"q": key_pair.q,
		"n": key_pair.public.modulus,
		"phi": (key_pair.p - 1) * (key_pair.q - 1),
		"e": key_pair.public.exponent,
		"d": key_pair.private.exponent,
	}
