"""Module providing a function printing python version 3.11.9"""
import logging

from enum import Enum

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from assymetric_cryptography import decrypt_with_asymmetric_method

logging.basicConfig(level=logging.DEBUG)


class Mode(Enum):
    """
    Attributes
    ----------
    generate: int
        So you need to generate keys
    encrypt: int
        So you need to encrypt the text
    decrypt: int
        So you need to decrypt the text
    """
    GENERATE = 0
    ENCRYPT = 1
    DECRYPT = 2


def write(path: str, text: bytes)->None:
    """
    ## Description:
    This function writes the provided text to the specified file path in binary mode.

    ## Arguments:
    - path (str): A string representing the file path where the text will be written.
    - text (bytes): A bytes object containing the text to be written to the file.

    ## Returns:
    - None
    """
    try:
        with open(path, "wb") as f:
            f.write(text)
    except Exception as e:
        logging.exception(e)


def read(path: str)->bytes:
    """
    ## Description:
    This function reads the contents of the specified file path in binary mode
    and returns the read bytes.

    ## Arguments:
    - path: A string representing the file path from where to read the contents.

    ## Returns:
    - A bytes object containing the read contents of the file.
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        logging.exception(e)


def serialisation_public_key(path: str, key)->None:
    """
    ## Description:
    Serialize a public key to a PEM file.

    ## Arguments:
    - path: str, path where the public key should be stored.
    - key: public key object.

    ## Returns:
    - None
    """
    write(path, key.public_bytes(encoding=serialization.Encoding.PEM,
                                 format=serialization.PublicFormat.SubjectPublicKeyInfo))


def serialisation_secret_key(path: str, key)->None:
    """
    ## Description:
    Serialize an cecret key to a PEM file.

    ## Arguments:
    - path: str, path where the key should be stored.
    - key: secret key object.

    ## Returns:
    - None
    """
    write(path, key.private_bytes(encoding=serialization.Encoding.PEM,
                                  format=serialization.PrivateFormat.TraditionalOpenSSL,
                                  encryption_algorithm=serialization.NoEncryption()))


def deserialisation_secret_key(path: str):
    """
    ## Description:
    Deserialize a secret key from a PEM file.

    ## Arguments:
    - path: str, path to the secret key.

    ## Returns:
    - secret key object
    """
    return load_pem_private_key(read(path), password=None)


def encrypt_and_serialisation_symmetryc_key(path: str, symmetric_key: bytes, public_key)->None:
    """
    ## Description:
    Encrypt a symmetric key with a public key and serialize to a file.

    ## Arguments:
    - path: str, path where the encrypted key should be stored.
    - symmetric_key: bytes, symmetric key to encrypt and serialize.
    - public_key: public key used for encryption.

    ## Returns:
    - None
    """
    write(path, public_key.encrypt(symmetric_key,
                                   asymmetric.padding.OAEP(
                                       mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
                                       algorithm=hashes.SHA256(),
                                       label=None,
                                   )
                                  )
         )


def decrypt_and_deserialisation_symmetryc_key(path_secret_key: str, path_symmetric_key: bytes):
    """
    Decrypt and deserialize a symmetric key using a secret key.

    ## Arguments:
    - path_secret_key: str, path to the secret key file.
    - path_symmetric_key: bytes, encrypted symmetric key.

    ## Returns:
    - decrypted symmetric key
    """
    secret_key = deserialisation_secret_key(path_secret_key)
    return decrypt_with_asymmetric_method(secret_key, read(path_symmetric_key))
