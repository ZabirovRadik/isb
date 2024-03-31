"""Module providing a function printing python version 3.11.8"""
import os
import json
import logging

from cryptography.hazmat.primitives.ciphers.algorithms import CAST5
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from write_read import write

logging.basicConfig(level=logging.DEBUG)


def  encrypt_with_asymmetric_method(public_key: rsa.RSAPublicKey, text: bytes)-> bytes:
    return public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))


def  decrypt_with_asymmetric_method(secret_key: rsa.RSAPublicKey, text: bytes)-> bytes:
    return secret_key.decrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))



def generate_and_save_keys(k_size: int,
                           for_public: str,
                           for_secret: str,
                           for_encrypted_symmetrycal: str
                           )->None:
    """
    ## Description:
    Function to generate keys - public key, private key, and encrypted symmetric key

    ## Arguments:
    - k_size (int): Size of the symmetric key
    - for_public (str): Path to save public key
    - for_secret (str): Path to save private key
    - for_encrypted_symmetrycal (str): Path to save encrypted symmetric key
    ## Returns:
    - None
    """
    if((k_size < 40 | k_size > 128) & k_size % 8 != 0):
        logging.exception("Uncorrect key's size")
    symmetric_key = os.urandom(k_size // 8)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    write(for_public, public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PublicFormat.SubjectPublicKeyInfo))
    write(for_secret, private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                encryption_algorithm=serialization.NoEncryption()))
    write(for_encrypted_symmetrycal, 
          public_key.encrypt(symmetric_key,
                             padding.OAEP(
                                          mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                          algorithm=hashes.SHA256(),
                                          label=None,
                                          ),
                            )
          )
