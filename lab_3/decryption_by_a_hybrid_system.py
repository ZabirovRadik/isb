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


def decript_by_hybrid(encrypted_text: str,
                      secret_key: rsa.RSAPublicKey,
                      path_key_of_symmetric: str,
                      path_to_save: str
                      )->bytes:
    """
    ## Description:
    Function to decrypt text using a hybrid method

    ## Arguments:
    - encrypted_text (str): A string containing the plaintext to be encrypted.
    - secret_key (rsa.RSAPublicKey): An RSAPublicKey object representing the path to the RSA public key used for decryption.
    - path_key_of_symmetric (str): A string representing the path to the symmetric key file used for encryption.
    - path_to_save (str): A string representing the path to save the decrypted text.

    ## Returns:
    - A bytes object representing the encrypted text.
    """
    private_bytes = read(secret_key)
    d_private_key = load_pem_private_key(private_bytes, password= None)
    encrypted_key = read(path_key_of_symmetric)
    text = read(encrypted_text)
    iv = text[:8]
    text = text[8:]
    try:
        key = decrypt_with_asymmetric_method(d_private_key,
                                            encrypted_key)
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        unpadder =  padding.ANSIX923(len(key) * 8).unpadder()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    except Exception as e:
         logging.exception(e)
    write(path_to_save, unpadded_dc_text)
    return unpadded_dc_text
