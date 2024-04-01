"""Module providing a function printing python version 3.11.8"""
import argparse
import os
import logging
import json

from enum import Enum

from generate_keys import generate_and_save_keys
from encryption_by_a_hybrid_system import encript_by_hybrid
from decryption_by_a_hybrid_system import decript_by_hybrid

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


if __name__ == "__main__":
    try:
        with open(os.path.join("lab_3", "json", "settings.json"),
                    mode = "r",
                    encoding = "utf-8") as f:
                file = json.load(f)
    except Exception as e:
         logging.exception(e)
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',
                       '--mode',
                       type= int,
                       default= Mode.DECRYPT,
                       help= 'Выбор режима работы')
    args = parser.parse_args()
    match args.mode:
        case Mode.GENERATE:
            generate_and_save_keys(file["key_size"],
                           os.path.join(file["main_folder"],
                                        file["keys"],
                                        file["public_key"]),
                           os.path.join(file["main_folder"],
                                        file["keys"],
                                        file["secret_key"]),
                           os.path.join(file["main_folder"],
                                        file["keys"],
                                        file["symmetric_key"])
                           )
        case Mode.ENCRYPT:
              encript_by_hybrid(
                                os.path.join(file["main_folder"],
                                            file["files"],
                                            file["initial_file"]),
                                os.path.join(file["main_folder"],
                                            file["keys"],
                                            file["secret_key"]),
                                os.path.join(file["main_folder"],
                                            file["keys"],
                                            file["symmetric_key"]),
                                os.path.join(file["main_folder"],
                                            file["files"],
                                            file["encrypted_file"])
                                )
        case Mode.DECRYPT:
               decript_by_hybrid(
                                os.path.join(file["main_folder"],
                                            file["files"],
                                            file["encrypted_file"]),
                                os.path.join(file["main_folder"],
                                            file["keys"],
                                            file["secret_key"]),
                                os.path.join(file["main_folder"],
                                            file["keys"],
                                            file["symmetric_key"]),
                                os.path.join(file["main_folder"],
                                            file["files"],
                                            file["decrypted_file"])
                                )