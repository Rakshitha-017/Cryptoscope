import pytest

from crypto.diffie_hellman import (
	calculate_public_key,
	calculate_shared_secret,
	exchange_values,
	DHParameters,
)
from crypto.rsa import decrypt, encrypt, generate_keypair, intermediate_values, sign, verify
from crypto.sha256 import hash_bytes, hash_text, sha256
from utils.helpers import bytes_to_int, int_to_bytes, text_to_bytes
from utils.math import (
	extended_gcd,
	gcd,
	is_prime,
	modular_exponentiation,
	modular_inverse,
)


def test_math_primitives_and_edge_cases():
	assert modular_exponentiation(4, 13, 497) == 445
	assert gcd(84, 30) == 6
	common, first_coefficient, second_coefficient = extended_gcd(240, 46)
	assert common == 2
	assert 240 * first_coefficient + 46 * second_coefficient == common
	assert modular_inverse(3, 11) == 4
	assert is_prime(97)
	assert not is_prime(1)
	assert not is_prime(91)

	with pytest.raises(ValueError):
		modular_exponentiation(2, 3, 0)
	with pytest.raises(ValueError):
		modular_inverse(2, 4)


def test_helper_conversions_round_trip():
	data = text_to_bytes("Cryptoscope")
	assert int_to_bytes(bytes_to_int(data)) == data
	assert int_to_bytes(0) == b"\x00"
	with pytest.raises(ValueError):
		int_to_bytes(-1)


def test_rsa_round_trip_signature_and_intermediate_values():
	key_pair = generate_keypair(61, 53)
	message = 42
	ciphertext = encrypt(message, key_pair.public)

	assert decrypt(ciphertext, key_pair.private) == message
	signature = sign(message, key_pair.private)
	assert verify(message, signature, key_pair.public)
	assert intermediate_values(key_pair)["phi"] == 3120

	with pytest.raises(ValueError):
		encrypt(key_pair.public.modulus, key_pair.public)
	with pytest.raises(ValueError):
		decrypt(key_pair.private.modulus, key_pair.private)
	with pytest.raises(ValueError):
		generate_keypair(61, 61)


def test_diffie_hellman_participants_derive_same_secret():
	parameters = DHParameters(prime=23, generator=5)
	values = exchange_values(6, 15, parameters)
	assert values["shared_secret"] == values["other_shared_secret"]
	assert calculate_public_key(6, 5, 23) == 8
	assert calculate_shared_secret(6, values["other_public_key"], 23) == 2

	with pytest.raises(ValueError):
		calculate_public_key(1, 5, 23)
	with pytest.raises(ValueError):
		calculate_public_key(6, 5, 21)


def test_sha256_known_vectors_for_text_and_bytes():
	expected_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
	expected_abc = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
	assert hash_text("") == expected_empty
	assert hash_text("abc") == expected_abc
	assert hash_bytes(b"abc") == expected_abc
	assert sha256("abc") == expected_abc
