"""Module providing a function printing python version 3.11.9"""
import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

logging.basicConfig(level=logging.DEBUG)


def  encrypt_with_asymmetric_method(public_key: rsa.RSAPublicKey, text: bytes)-> bytes:
    """
    ## Description:
    Encrypts the given text using asymmetric encryption with the provided public key.

    ## Arguments:
    - public_key (rsa.RSAPublicKey): The RSA public key used for encryption.
    - text (bytes): The plaintext bytes to be encrypted.

    ## Returns:
    - bytes: The encrypted ciphertext.
    """
    return public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))


def  decrypt_with_asymmetric_method(secret_key: rsa.RSAPublicKey, text: bytes)-> bytes:
    """
    ## Description:
    Decrypts the given ciphertext using asymmetric decryption with the provided private key.

    ## Arguments:
    - secret_key (rsa.RSAPrivateKey): The RSA private key used for decryption.
    - text (bytes): The ciphertext bytes to be decrypted.

    ## Returns:
    - bytes: The decrypted plaintext.
    """
    return secret_key.decrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))
