import cryptography
from cryptography.hazmat.primitives.ciphers.algorithms import CAST5
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os


def  encrypt_with_asymmetric_method(public_key: rsa.RSAPublicKey, text: bytes):
    return public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))

def generate_and_save_keys(k_size: int,
                           for_public: str,
                           for_secret: str,
                           for_encrypted_symmetrycal: str
                           )->None:
    symmetric_key = os.urandom(k_size//8)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=k_size)
    public_key = private_key.public_key()
    with open(for_public, 'wb') as public_out:
        public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
             format=serialization.PublicFormat.SubjectPublicKeyInfo))
    with open(for_secret, 'wb') as private_out:
        private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
              format=serialization.PrivateFormat.TraditionalOpenSSL,
              encryption_algorithm=serialization.NoEncryption()))
    with open(for_encrypted_symmetrycal,'wb') as encr_sym:
        encr_sym.write(symmetric_key.encrypt(
                public_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            ))
    