"""Module providing a function printing python version 3.11.9"""
import os
import logging

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


logging.basicConfig(level=logging.DEBUG)


def encrypt_with_symmetric_method(key: bytes, text: bytes) -> bytes:
    """
    ## Description:
    Encrypts the given text using symmetric encryption with the provided key. Uses CAST5 cipher and CBC mode.

    ## Arguments:
    - key (bytes): The symmetric key to use for encryption.
    - text (bytes): The plaintext to encrypt.

    ## Returns:
    - bytes: The encrypted ciphertext.
    """
    iv = os.urandom(8)
    try:
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.ANSIX923(len(key) * 8).padder()
        padded_text = padder.update(text) + padder.finalize()
        c_text = iv + encryptor.update(padded_text) + encryptor.finalize()
    except Exception as e:
        logging.exception(e)
    return c_text


def decrypt_with_symmetric_method(key: bytes, text: bytes) -> bytes:
    """
    ## Description:
    Decrypts the given ciphertext using symmetric decryption with the provided key. Uses CAST5 cipher and CBC mode.

    ## Arguments:
    - key (bytes): The symmetric key to use for decryption.
    - text (bytes): The ciphertext to decrypt.

    ## Returns:
    - bytes: The decrypted plaintext.
    """
    iv = text[:8]
    text = text[8:]
    try:
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        unpadder = padding.ANSIX923(len(key) * 8).unpadder()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    except Exception as e:
        logging.exception(e)
    return unpadded_dc_text