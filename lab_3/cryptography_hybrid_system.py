"""Module providing a function printing python version 3.11.9"""
import logging
import os

from cryptography.hazmat.primitives import asymmetric

from auxiliary_operations import read, write, serialisation_secret_key, serialisation_public_key, \
    encrypt_and_serialisation_symmetryc_key, decrypt_and_deserialisation_symmetryc_key
from symmetric_cryptography import encrypt_with_symmetric_method, decrypt_with_symmetric_method

logging.basicConfig(level=logging.DEBUG)


class Cryptograthy:
    """
    ## Description:
    Class of hybrid cryptosystem. Symmetric Triple Des encryption algorithm, Asymmetric RSA.

    ## Arguments:
    - generate_and_save_keys(self)->None
    - encript_by_hybrid(self, plain_text: str, path_to_save: str) -> None
    - decript_by_hybrid(self, encrypted_text: str, path_to_save: str)->None:
    """

    def __init__(self,
                 for_symmetrycal_key: str,
                 public_key: str,
                 secret_key: str
                 ) -> None:
        """
        ## Arguments:
        - for_public (str): Path to save public key
        - for_secret (str): Path to save private key
        - for_encrypted_symmetrycal (str): Path to save encrypted symmetric key
        """
        self.for_symmetrycal = for_symmetrycal_key
        self.for_public = public_key
        self.for_secret = secret_key

    def generate_and_save_keys(self,
                               k_size: int
                               )->None:
        """
        ## Description:
        Method to generate keys - public key, private key, and encrypted symmetric key

        ## Arguments:
        - k_size (int): Size of the symmetric key
        ## Returns:
        - None
        """
        if (k_size < 40 | k_size > 128) & k_size % 8 != 0:
            logging.exception("Incorrect key's size")
        symmetric_key = os.urandom(k_size // 8)
        secret = asymmetric.rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = secret.public_key()
        serialisation_public_key(self.for_public, public_key)
        serialisation_secret_key(self.for_secret, secret)
        encrypt_and_serialisation_symmetryc_key(self.for_symmetrycal, symmetric_key, public_key)

    def encript_by_hybrid(self,
                          plain_text: str,
                          path_to_save: str
                          )->bytes:
        """
        ## Description:
        This function encrypts the given plaintext using a hybrid
        encryption approach with RSA and CAST5 cipher algorithms.

        ## Arguments:
        - plain_text (str): A string containing the plaintext to be encrypted.
        - path_to_save (str): A string representing the path to save the encrypted text.

        ## Returns:
        - A bytes object representing the encrypted text.
        """
        key = decrypt_and_deserialisation_symmetryc_key(self.for_secret, self.for_symmetrycal)
        text = read(plain_text)
        c_text = encrypt_with_symmetric_method(key, text)
        write(path_to_save, c_text)
        return c_text

    def decript_by_hybrid(self,
                          encrypted_text: str,
                          path_to_save: str
                          )->bytes:
        """
        ## Description:
        Function to decrypt text using a hybrid method

        ## Arguments:
        - encrypted_text (str): A string containing the plaintext to be encrypted.
        - path_to_save (str): A string representing the path to save the decrypted text.

        ## Returns:
        - A bytes object representing the encrypted text.
        """
        key = decrypt_and_deserialisation_symmetryc_key(self.for_secret, self.for_symmetrycal)
        text = read(encrypted_text)
        unpadded_dc_text = decrypt_with_symmetric_method(key, text)
        write(path_to_save, unpadded_dc_text)
        return unpadded_dc_text
