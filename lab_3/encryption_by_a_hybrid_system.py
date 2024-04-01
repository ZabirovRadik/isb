"""Module providing a function printing python version 3.11.8"""
import os
import logging

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from write_read import read, write
from generate_keys import decrypt_with_asymmetric_method

logging.basicConfig(level=logging.DEBUG)


def encript_by_hybrid(plain_text: str,
                      secret_key: rsa.RSAPublicKey,
                      path_key_of_symmetric: str,
                      path_to_save: str
                      )->bytes:
    """
    ## Description:
    This function encrypts the given plaintext using a hybrid encryption approach with RSA and CAST5 cipher algorithms.

    ## Arguments:
    - plain_text (str): A string containing the plaintext to be encrypted.
    - secret_key (rsa.RSAPublicKey): An RSAPublicKey object representing the path to the RSA public key used for encryption.
    - path_key_of_symmetric (str): A string representing the path to the symmetric key file used for encryption.
    - path_to_save (str): A string representing the path to save the encrypted text.

    ## Returns:
    - A bytes object representing the encrypted text.
    """
    private_bytes = read(secret_key)
    d_private_key = load_pem_private_key(private_bytes, password= None)
    encrypted_key = read(path_key_of_symmetric)
    text = read(plain_text)
    iv = os.urandom(8)
    try:
        key = decrypt_with_asymmetric_method(d_private_key,
                                            encrypted_key)
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.ANSIX923(len(key)*8).padder()
        padded_text = padder.update(text) + padder.finalize()
        c_text = iv + encryptor.update(padded_text) + encryptor.finalize()
    except Exception as e:
        logging.exception(e)
    write(path_to_save, c_text)
    return c_text
