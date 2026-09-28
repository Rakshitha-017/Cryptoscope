"""Interactive command-line runner for the educational RSA and DH demos."""

from __future__ import annotations

from crypto.diffie_hellman import calculate_public_key, calculate_shared_secret
from crypto.rsa import decrypt, encrypt, generate_keypair


def run_rsa() -> None:
    """Read RSA demo parameters and print the encryption round trip."""
    p = int(input("Enter prime p (example 61): "))
    q = int(input("Enter prime q (example 53): "))
    message = int(input("Enter an integer message smaller than p*q: "))
    key_pair = generate_keypair(p, q)
    ciphertext = encrypt(message, key_pair.public)
    plaintext = decrypt(ciphertext, key_pair.private)
    print(f"Public key: (e={key_pair.public.exponent}, n={key_pair.public.modulus})")
    print(f"Private key: (d={key_pair.private.exponent}, n={key_pair.private.modulus})")
    print(f"Encrypted message: {ciphertext}")
    print(f"Decrypted message: {plaintext}")


def run_diffie_hellman() -> None:
    """Read Diffie-Hellman parameters and print both shared secrets."""
    prime = int(input("Enter a prime number: "))
    generator = int(input("Enter a generator: "))
    alice_private = int(input("Enter Alice's private key: "))
    bob_private = int(input("Enter Bob's private key: "))
    alice_public = calculate_public_key(alice_private, generator, prime)
    bob_public = calculate_public_key(bob_private, generator, prime)
    alice_secret = calculate_shared_secret(alice_private, bob_public, prime)
    bob_secret = calculate_shared_secret(bob_private, alice_public, prime)
    print(f"Alice public key: {alice_public}")
    print(f"Bob public key: {bob_public}")
    print(f"Alice shared secret: {alice_secret}")
    print(f"Bob shared secret: {bob_secret}")
    print(f"Secrets match: {alice_secret == bob_secret}")


def main() -> None:
    """Show the demo menu and run the selected algorithm."""
    print("1. RSA")
    print("2. Diffie-Hellman")
    choice = input("Choose an algorithm: ").strip()
    if choice == "1":
        run_rsa()
    elif choice == "2":
        run_diffie_hellman()
    else:
        raise ValueError("choose 1 for RSA or 2 for Diffie-Hellman")


if __name__ == "__main__":
    main()