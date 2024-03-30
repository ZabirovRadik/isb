import argparse
import cryptography
import json

from enum import Enum

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-m',
                       '--mode',
                       type= int,
                       default= Mode.GENERATE,
                       help= 'Выбор режима работы')
    args = parser.parse_args()